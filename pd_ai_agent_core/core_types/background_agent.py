from abc import ABC, abstractmethod
from typing import Optional, Set
from pd_ai_agent_core.messages.background_message import BackgroundMessage
from pd_ai_agent_core.helpers.strings import normalize_string


class BackgroundAgent(ABC):
    def __init__(
        self, session_id: str, agent_type: str, interval: Optional[float] = None
    ):
        self.session_id = session_id
        self._agent_type = agent_type
        self.interval = interval
        self.agent_className = self.__class__.__name__
        self.subscribed_messages: Set[str] = set()
        self._is_running = False
        self._name = ""

    @abstractmethod
    async def process(self) -> None:
        """Process timer-based work"""
        pass

    @abstractmethod
    async def process_message(self, message: BackgroundMessage) -> None:
        """Process message-based work"""
        pass

    def subscribe_to(self, message_type: str) -> None:
        """Subscribe to a message type (supports wildcards)"""
        self.subscribed_messages.add(message_type)

    @property
    def agent_type(self) -> str:
        """Unique identifier for this type of agent"""
        return self._agent_type

    @property
    def session_id(self) -> str:
        """Get the session ID for this agent"""
        return self._session_id

    @session_id.setter
    def session_id(self, value: str) -> None:
        """Set the session ID for this agent"""
        self._session_id = value

    @property
    def name(self) -> str:
        """Get the name of the agent"""
        return self._name

    @property
    def id(self) -> str:
        """Get the ID of the agent"""
        return normalize_string(self._name)
