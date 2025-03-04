from typing import Optional, Dict, Any
from pd_ai_agent_core.messages.message import Message
from websockets.legacy.server import WebSocketServerProtocol
import json
import uuid
from pd_ai_agent_core.services.session_manager import SessionManager
from pd_ai_agent_core.messages.error_message import create_error_message
from pd_ai_agent_core.messages.event_message import create_event_message
from pd_ai_agent_core.messages.error_message import create_error_message_from_message
import logging
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from pd_ai_agent_core.common.constants import GLOBAL_CHANNEL, NOTIFICATION_SERVICE_NAME
from pd_ai_agent_core.core_types.session_service import SessionService
from pd_ai_agent_core.services.service_registry import ServiceRegistry

logger = logging.getLogger(__name__)


class NotificationService(SessionService):
    def __init__(
        self,
        session_id: str,
        websocket: WebSocketServerProtocol,
        debug: bool = False,
    ):
        self._session_id = session_id
        self._session_manager = SessionManager.get_instance()
        self._connection = websocket
        self._debug = debug
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._notification_queue: Queue = Queue()
        self._should_process = True
        self._main_loop = asyncio.get_event_loop()  # Store the main event loop
        self._start_queue_processor()
        self.register()

    def name(self) -> str:
        return NOTIFICATION_SERVICE_NAME

    def register(self) -> None:
        """Register this service with the registry"""
        if not ServiceRegistry.register(
            self._session_id, NOTIFICATION_SERVICE_NAME, self
        ):
            logger.info(
                f"Notification service already registered for session {self._session_id}"
            )
            return

    def unregister(self) -> None:
        """Unregister this service from the registry"""
        self.stop_queue_processor()
        logger.info(f"Notification service unregistered for session {self._session_id}")

    def update_websocket(self, websocket: WebSocketServerProtocol):
        """Update the websocket connection"""
        self._connection = websocket

    def _handle_send_result(self, future):
        """Handle the result of the send operation"""
        try:
            future.result()
        except Exception as e:
            logger.error(f"Error in send operation: {e}")

    def _start_queue_processor(self):
        """Start the background thread for processing notifications"""

        async def process_notifications_async():
            while self._should_process:
                try:
                    if not self._notification_queue.empty():
                        notification = (
                            self._notification_queue.get_nowait()
                        )  # Changed to non-blocking
                        try:
                            # Schedule the send operation on the main loop
                            future = asyncio.run_coroutine_threadsafe(
                                self.send(notification), self._main_loop
                            )
                            # Don't wait for the result, let it run independently
                            future.add_done_callback(
                                lambda f: self._handle_send_result(f)
                            )
                        except Exception as e:
                            logger.error(f"Error sending notification: {e}")
                    await asyncio.sleep(0.01)  # Reduced sleep time
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    logger.error(f"Error in notification processor: {e}")

        def run_async_loop():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(process_notifications_async())
            finally:
                loop.close()

        self._processor_thread = threading.Thread(target=run_async_loop, daemon=True)
        self._processor_thread.start()

    def stop_queue_processor(self):
        """Stop the queue processor thread"""
        self._should_process = False
        if hasattr(self, "_processor_thread"):
            self._processor_thread.join(timeout=5)  # Wait for thread to finish

    def queue_notification(self, message: Message):
        """Add a notification to the queue"""
        if not self._should_process:
            logger.warning("Queue processor is stopped, message will not be processed")
            return
        self._notification_queue.put(message)
        logger.debug(f"Queued notification: {message.to_dict()}")

    def send_sync(self, message: Message):
        """Queue a message for sending"""
        self.queue_notification(message)

    def send_error_sync(self, channel: Optional[str], error: str):
        """Queue an error message"""
        error_message = create_error_message(
            session_id=self._session_id,
            channel=channel if channel is not None else str(uuid.uuid4()),
            error_message=error,
        )
        self.queue_notification(error_message)

    def send_event_sync(
        self,
        channel: Optional[str],
        event: str,
        event_type: Optional[str],
        event_data: Dict[str, Any] | list[Dict[str, Any]] | None = None,
    ):
        """Queue an event message"""
        event_message = create_event_message(
            self._session_id, channel, event, event_type, event_data
        )
        self.queue_notification(event_message)

    async def send(self, message: Message) -> bool:
        """Send a message to a specific session"""
        if not self._session_manager.is_session_valid(message.session_id):
            return False

        websocket = self._connection
        if not websocket:
            return False

        try:
            dict_message = message.to_dict()
            await websocket.send(json.dumps(dict_message))
            if self._debug:
                logger.info(f"Sent message: {dict_message}")
            return True
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False

    async def send_event(
        self,
        channel: Optional[str],
        event: str,
        event_type: Optional[str],
        event_data: Dict[str, Any] | list[Dict[str, Any]] | None = None,
    ):
        """Send an event message to a specific session"""
        event_message = create_event_message(
            self._session_id, channel, event, event_type, event_data
        )
        await self.send(event_message)
        if self._debug:
            logger.debug(f"Sent event message: {event_message.to_dict()}")

    async def send_error(self, channel: Optional[str], error: str):
        """Send an error message to a specific session"""
        error_message = create_error_message(
            session_id=self._session_id,
            channel=channel if channel is not None else str(uuid.uuid4()),
            error_message=error,
        )

        await self.send(error_message)
        if self._debug:
            logger.debug(f"Sent error message: {error_message.to_dict()}")

    async def send_exception(
        self,
        e: Exception,
        message: Message | None = None,
        channel: Optional[str] = None,
    ):
        """Send an error message to a specific session"""
        if message is not None:
            error_message = create_error_message_from_message(
                message, error_message=str(e)
            )
        else:
            error_message = create_error_message(
                session_id=self._session_id,
                channel=channel if channel is not None else str(uuid.uuid4()),
                error_message=str(e),
            )
        await self.send(error_message)
        if self._debug:
            logger.debug(f"Sent exception message: {error_message.to_dict()}")

    async def broadcast(self, message: Message):
        """Broadcast a message to all active sessions"""
        try:
            if self._session_manager.is_session_valid(self._session_id):
                broadcast_message = Message(
                    session_id=self._session_id,
                    channel=GLOBAL_CHANNEL,
                    subject=message.subject,
                    body=message.body,
                    context=message.context,
                )
                await self.send(broadcast_message)
                if self._debug:
                    logger.debug(
                        f"Broadcasted message {message.to_dict()} to session {self._session_id}"
                    )
        except Exception as e:
            logger.error(f"Error broadcasting to session {self._session_id}: {e}")

    def broadcast_sync(self, message: Message):
        """Broadcast a message to all active sessions"""
        broadcast_message = Message(
            session_id=self._session_id,
            channel=GLOBAL_CHANNEL,
            subject=message.subject,
            body=message.body,
            context=message.context,
        )
        self.send_sync(broadcast_message)
        if self._debug:
            logger.debug(
                f"Broadcasted message {message.to_dict()} to session {self._session_id}"
            )
