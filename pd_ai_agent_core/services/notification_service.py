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
        self._main_loop = None  # We'll get the loop when needed rather than storing it
        self._connection_lock = threading.RLock()  # Add lock for thread-safety
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
        # First stop the queue processor
        self.stop_queue_processor()

        # Clear any pending messages
        try:
            while not self._notification_queue.empty():
                self._notification_queue.get_nowait()
        except Exception:
            pass

        # Close the connection
        with self._connection_lock:
            self._connection = None

        logger.info(f"Notification service unregistered for session {self._session_id}")

    def update_websocket(self, websocket: WebSocketServerProtocol):
        """Update the websocket connection"""
        with self._connection_lock:
            # Store the old websocket to check if it needs cleaning up
            old_websocket = self._connection

            # Update to the new websocket
            if websocket and self._connection != websocket:
                self._connection = websocket
                logger.info(
                    f"Updated websocket connection for session {self._session_id}"
                )

            # Return immediately if there was no old websocket or it's the same as the new one
            if not old_websocket or old_websocket == websocket:
                return

            # Try to clean up the old websocket if it's different
            try:
                # We don't actually close it here as that would be handled by the server
                logger.debug(
                    f"Old websocket connection replaced for session {self._session_id}"
                )
            except Exception as e:
                logger.error(f"Error handling old websocket: {e}")

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
                        notification = self._notification_queue.get_nowait()
                        try:
                            # Always run notifications directly in this loop
                            # This avoids crossing event loops
                            # The send method will handle making sure the message is sent
                            # in the right loop if necessary
                            await self.send(notification)
                        except Exception as e:
                            logger.error(f"Error processing notification: {e}")
                    await asyncio.sleep(0.01)  # Reduced sleep time
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    logger.error(f"Error in notification processor: {e}")

        def run_async_loop():
            # Create a new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # Store the loop for debugging purposes
            self._processor_loop = loop

            try:
                # Run until the notification processor is done
                loop.run_until_complete(process_notifications_async())
            except Exception as e:
                logger.error(f"Error in notification processor thread: {e}")
            finally:
                try:
                    # Close the loop gracefully
                    pending = asyncio.all_tasks(loop)
                    if pending:
                        loop.run_until_complete(
                            asyncio.gather(*pending, return_exceptions=True)
                        )
                    loop.close()
                except Exception as e:
                    logger.error(f"Error closing event loop: {e}")
                finally:
                    self._processor_loop = None

        self._processor_thread = threading.Thread(target=run_async_loop, daemon=True)
        self._processor_thread.start()

    def stop_queue_processor(self):
        """Stop the queue processor thread"""
        if not hasattr(self, "_should_process") or not self._should_process:
            return  # Already stopped

        # Signal thread to stop
        self._should_process = False

        # Wait for thread to finish with timeout
        if (
            hasattr(self, "_processor_thread")
            and self._processor_thread
            and self._processor_thread.is_alive()
        ):
            try:
                self._processor_thread.join(timeout=2.0)
            except Exception as e:
                logger.error(f"Error stopping processor thread: {e}")

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

        # Get websocket connection with lock
        with self._connection_lock:
            websocket = self._connection
            if not websocket:
                return False

            # Check if websocket is still open before attempting to send
            try:
                connection_open = not getattr(websocket, "closed", False)
                if hasattr(websocket, "open"):
                    connection_open = connection_open and websocket.open

                # Additional check for connection state
                if hasattr(websocket, "state") and hasattr(websocket.state, "name"):
                    connection_open = connection_open and websocket.state.name == "OPEN"

                if not connection_open:
                    logger.warning(
                        "Cannot send message: WebSocket connection appears to be closed"
                    )
                    return False
            except Exception as e:
                logger.debug(f"Could not check websocket status: {e}")

            # Create a local reference to use for sending
            current_websocket = websocket

        try:
            dict_message = message.to_dict()
            json_message = json.dumps(dict_message)

            # Simple direct send without shields or other complexity
            await current_websocket.send(json_message)

            if self._debug:
                logger.info(f"Sent message: {dict_message}")
            return True
        except asyncio.CancelledError:
            # Don't log cancelled errors as they're expected during shutdown
            return False
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
