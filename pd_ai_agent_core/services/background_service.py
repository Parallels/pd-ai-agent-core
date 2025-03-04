import asyncio
import logging
from typing import Dict, List
from datetime import datetime, timedelta
from fnmatch import fnmatch
from pd_ai_agent_core.core_types.background_agent import BackgroundAgent
from pd_ai_agent_core.core_types.session_service import SessionService
from pd_ai_agent_core.messages.background_message import BackgroundMessage
from pd_ai_agent_core.common.constants import BACKGROUND_SERVICE_NAME
from collections import deque
from pd_ai_agent_core.services.service_registry import ServiceRegistry
import concurrent.futures

logger = logging.getLogger(__name__)


class BackgroundAgentService(SessionService):
    def __init__(
        self,
        session_id: str,
        rate_limit_messages: int = 100,
        rate_limit_window: int = 60,
        debug: bool = False,
    ):
        self._agents: Dict[tuple[str, str], BackgroundAgent] = (
            {}
        )  # (session_id, agent_type) -> agent
        self._tasks: Dict[tuple[str, str], asyncio.Task] = {}
        self._message_queue: deque[BackgroundMessage] = deque()
        self._processing = False
        self._session_id = session_id
        self._rate_limit_messages = rate_limit_messages
        self._rate_limit_window = rate_limit_window
        self._message_timestamps: deque[datetime] = deque()
        self.debug = debug
        self._thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        self._main_loop = asyncio.get_event_loop()
        self._agent_loops: Dict[tuple[str, str], asyncio.AbstractEventLoop] = {}
        self.register()

    def name(self) -> str:
        return BACKGROUND_SERVICE_NAME

    def register(self) -> None:
        """Register this service with the registry"""
        if not ServiceRegistry.register(
            self._session_id, BACKGROUND_SERVICE_NAME, self
        ):
            logger.info(
                f"Background service already registered for session {self._session_id}"
            )
            return

    def unregister(self) -> None:
        """Unregister this service from the registry"""
        self.unregister_background_agent()
        logger.info(f"Background service unregistered for session {self._session_id}")

    async def add_background_agent(self, agent: BackgroundAgent) -> bool:
        """Add a new background agent if one doesn't exist for this session"""
        key = (agent.session_id, agent.agent_type)
        if key in self._agents:
            return False

        self._agents[key] = agent
        # Create a new event loop for this agent
        if agent.interval:
            self._tasks[key] = asyncio.create_task(self._run_agent_timer(agent))

        # Ensure message processing is running
        if not self._processing:
            self._processing = True
            asyncio.create_task(self._process_message_queue())

        return True

    def remove_background_agent(self, session_id: str, agent_type: str) -> bool:
        """Remove an agent and cancel its task"""
        key = (session_id, agent_type)
        if key not in self._agents:
            # Try to find the agent by session_id and agent_className
            found = False
            for k, v in self._agents.items():
                if k[0] == session_id and v.agent_className == agent_type:
                    key = k
                    found = True
                    break
            if not found:
                return False

        if key in self._tasks:
            self._tasks[key].cancel()
            del self._tasks[key]

        del self._agents[key]
        return True

    def unregister_background_agent(self):
        """Unregister all agents and stop the background service"""
        self._processing = False

        # Create a list of agents to avoid modifying dict during iteration
        agents_to_remove = [
            (agent.session_id, agent.agent_type) for agent in self._agents.values()
        ]

        # Remove each agent
        for session_id, agent_type in agents_to_remove:
            self.remove_background_agent(session_id, agent_type)

        # Clear all remaining data structures
        self._agents.clear()
        self._tasks.clear()
        self._message_queue.clear()
        self._message_timestamps.clear()

    def post_message(self, message_type: str, data: dict) -> None:
        """Synchronous method to post a message to the queue"""
        if not self._check_rate_limit():
            logger.warning("Rate limit exceeded, message dropped")
            return

        message = BackgroundMessage(message_type=message_type, data=data)
        self._message_queue.append(message)
        self._message_timestamps.append(datetime.now())
        logger.info(f"Message queued: {message_type}")

    def _check_rate_limit(self) -> bool:
        """Check if we're within rate limits"""
        now = datetime.now()
        cutoff = now - timedelta(seconds=self._rate_limit_window)

        # Remove old timestamps
        while self._message_timestamps and self._message_timestamps[0] < cutoff:
            self._message_timestamps.popleft()

        return len(self._message_timestamps) < self._rate_limit_messages

    async def _run_agent_timer(self, agent: BackgroundAgent):
        """Run the agent's process function at specified intervals"""
        # key = (agent.session_id, agent.agent_type)
        while True:
            if agent.interval is None:
                await asyncio.sleep(0)
            else:
                try:
                    # Run agent process in thread pool
                    await self._main_loop.run_in_executor(
                        self._thread_pool, lambda: asyncio.run(agent.process())
                    )
                except Exception as e:
                    logger.error(
                        f"Error in agent {agent.agent_type} for session {agent.session_id}: {e}"
                    )
            await asyncio.sleep(agent.interval or 0)

    async def _process_message_queue(self):
        """Process messages from the queue"""
        while self._processing:
            if self._message_queue:
                message = self._message_queue.popleft()
                logger.info(f"Processing message: {message.message_type}")
                await self._distribute_message(message)
            await asyncio.sleep(0.1)

    async def _distribute_message(self, message: BackgroundMessage):
        """Distribute a message to all subscribed agents"""
        tasks = []

        for agent in self._agents.values():
            for pattern in agent.subscribed_messages:
                if fnmatch(message.message_type, pattern):
                    # Create task for each agent that should process the message
                    task = asyncio.create_task(
                        self._process_agent_message(agent, message)
                    )
                    tasks.append(task)
                    break  # Agent matched, no need to check other patterns

        if tasks:
            # Wait for all agent tasks to complete
            await asyncio.gather(*tasks)

    async def _process_agent_message(
        self, agent: BackgroundAgent, message: BackgroundMessage
    ):
        """Process a message for a single agent with retry logic in a separate thread"""

        async def process_with_retries():
            while message.retry_count < message.max_retries:
                try:
                    await agent.process_message(message)
                    return
                except Exception as e:
                    message.retry_count += 1
                    logger.error(
                        f"Error processing message {message.message_type} in agent {agent.agent_type} "
                        f"(attempt {message.retry_count}/{message.max_retries}): {e}"
                    )
                    if message.retry_count < message.max_retries:
                        await asyncio.sleep(1 * message.retry_count)

        try:
            # Run the processing in a thread pool
            await self._main_loop.run_in_executor(
                self._thread_pool, lambda: asyncio.run(process_with_retries())
            )
        except Exception as e:
            logger.error(f"Error in thread pool execution: {e}")

    def get_agents(self) -> List[BackgroundAgent]:
        """Get all registered agents"""
        return list(self._agents.values())
