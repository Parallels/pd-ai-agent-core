from typing import Optional, Dict, Any
from pd_ai_agent_core.messages.message import Message
from websockets.legacy.server import WebSocketServerProtocol
import json
import uuid
import zlib
import base64
import time
from pd_ai_agent_core.services.session_manager import SessionManager
from pd_ai_agent_core.messages.error_message import create_error_message
from pd_ai_agent_core.messages.event_message import create_event_message
from pd_ai_agent_core.messages.error_message import create_error_message_from_message
import logging
import asyncio
import threading
from queue import Queue
from pd_ai_agent_core.common.constants import (
    GLOBAL_CHANNEL,
    NOTIFICATION_SERVICE_NAME,
)
from pd_ai_agent_core.core_types.session_service import SessionService
from pd_ai_agent_core.services.service_registry import ServiceRegistry

logger = logging.getLogger(__name__)

# Default compression level (0-9, where 9 is highest compression)
DEFAULT_COMPRESSION_LEVEL = 6

# Size threshold in bytes - messages larger than this will be compressed
DEFAULT_COMPRESSION_THRESHOLD = 1024  # 1KB

# Default message polling interval in seconds
DEFAULT_POLLING_INTERVAL = 0.01  # 10ms


class NotificationService(SessionService):
    def __init__(
        self,
        session_id: str,
        websocket: WebSocketServerProtocol,
        debug: bool = False,
        compression_enabled: bool = False,
        compression_level: int = DEFAULT_COMPRESSION_LEVEL,
        compression_threshold: int = DEFAULT_COMPRESSION_THRESHOLD,
        polling_interval: float = DEFAULT_POLLING_INTERVAL,
    ):
        self._session_id = session_id
        self._session_manager = SessionManager.get_instance()
        self._connection = websocket
        self._debug = debug
        self._notification_queue: Queue = Queue()
        self._should_process = True
        self._connection_lock = threading.RLock()  # Lock for thread-safety
        self._event_loop = asyncio.get_event_loop()  # Store the main event loop

        # Compression settings
        self._compression_enabled = compression_enabled
        self._compression_level = compression_level
        self._compression_threshold = compression_threshold

        # Polling interval for the message processor
        self._polling_interval = polling_interval

        # Start the background thread for processing messages
        self._start_message_processor()
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
        # First stop the message processor
        self.stop_message_processor()

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

    def _start_message_processor(self):
        """Start a background thread to process and send messages from the queue"""

        def process_messages():
            """Thread function to process and send messages"""
            logger.info(f"Message processor started for session {self._session_id}")

            while self._should_process:
                try:
                    # Check if there are messages to process
                    if not self._notification_queue.empty():
                        # Get a message from the queue
                        message = self._notification_queue.get_nowait()

                        try:
                            # Process and send the message using the main event loop
                            self._send_message_in_main_loop(message)
                        except Exception as e:
                            logger.error(f"Error processing message: {e}")

                        # Mark the task as done
                        self._notification_queue.task_done()

                    # Sleep for a short time before checking again
                    time.sleep(self._polling_interval)

                except Exception as e:
                    logger.error(f"Error in message processor: {e}")
                    # Sleep briefly to avoid tight loops in case of persistent errors
                    time.sleep(0.5)

            logger.info(f"Message processor stopped for session {self._session_id}")

        # Create and start the background thread
        self._processor_thread = threading.Thread(target=process_messages, daemon=True)
        self._processor_thread.start()

    def _send_message_in_main_loop(self, message: Message):
        """Send a message in the main event loop"""
        with self._connection_lock:
            websocket = self._connection
            if not websocket:
                logger.warning(
                    f"Cannot send message: No websocket connection for session {self._session_id}"
                )
                return False

            # Check if the websocket connection is still valid
            try:
                connection_open = not getattr(websocket, "closed", False)
                if hasattr(websocket, "open"):
                    connection_open = connection_open and websocket.open

                if hasattr(websocket, "state") and hasattr(websocket.state, "name"):
                    connection_open = connection_open and websocket.state.name == "OPEN"

                if not connection_open:
                    logger.warning(
                        "Cannot send message: WebSocket connection appears to be closed"
                    )
                    return False
            except Exception as e:
                logger.debug(f"Could not check websocket status: {e}")
                return False

        try:
            # Prepare the message for sending
            dict_message = message.to_dict()
            json_message = json.dumps(dict_message)
            logger.debug(f"Sending message: {json_message}")

            # Compress the JSON data if enabled
            data_to_send, is_compressed, original_size, compressed_size = (
                self._compress_data(json_message)
            )

            # Create the final message to send
            if is_compressed:
                # Wrap compressed data in a metadata envelope
                wrapper = {
                    "compressed": True,
                    "encoding": "zlib+base64",
                    "size": {"original": original_size, "compressed": compressed_size},
                    "data": data_to_send,
                }
                final_message = json.dumps(wrapper)

                if self._debug:
                    compression_ratio = (1 - (compressed_size / original_size)) * 100
                    logger.info(
                        f"Compressed message: {original_size:,} bytes → {compressed_size:,} bytes ({compression_ratio:.1f}% reduction)"
                    )
            else:
                # Send uncompressed data directly
                final_message = json_message

            # Create a future to schedule the send operation in the main event loop
            future = asyncio.run_coroutine_threadsafe(
                websocket.send(final_message), self._event_loop
            )

            # Try with retries
            max_retries = 10
            retry_count = 0
            while retry_count < max_retries:
                try:
                    future.result(timeout=5.0)
                    return True
                except TimeoutError:
                    retry_count += 1
                    if retry_count >= max_retries:
                        raise
                    logger.warning(
                        f"Send operation timed out, retrying ({retry_count}/{max_retries})"
                    )
                    time.sleep(1)  # Add delay between retries

        except asyncio.CancelledError:
            # Don't log cancelled errors as they're expected during shutdown
            return False
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False

    def stop_message_processor(self):
        """Stop the message processor thread"""
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
            logger.warning(
                "Message processor is stopped, message will not be processed"
            )
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

    def _compress_data(self, data: str) -> tuple[str, bool, int, int]:
        """Compress string data using zlib and base64 encode it for safe transmission.

        Args:
            data: The string data to compress

        Returns:
            tuple containing:
            - The compressed and encoded data
            - Whether compression was applied
            - Original size in bytes
            - Compressed size in bytes
        """
        original_size = len(data)

        # Skip compression for small messages
        if (
            not self._compression_enabled
            or original_size <= self._compression_threshold
        ):
            return data, False, original_size, original_size

        try:
            # Compress the data
            compressed_data = zlib.compress(
                data.encode("utf-8"), level=self._compression_level
            )

            # Base64 encode for safe transmission
            encoded_data = base64.b64encode(compressed_data).decode("utf-8")
            compressed_size = len(encoded_data)

            # Only use compression if it actually reduces the size
            if compressed_size < original_size:
                return encoded_data, True, original_size, compressed_size
            else:
                # Compression didn't help, return original
                return data, False, original_size, original_size

        except Exception as e:
            logger.error(f"Compression error: {e}, sending uncompressed")
            return data, False, original_size, original_size

    async def send(self, message: Message) -> bool:
        """Send a message directly (async version)"""
        # Queue the message instead of sending directly to avoid event loop issues
        self.queue_notification(message)
        return True

    async def send_event(
        self,
        channel: Optional[str],
        event: str,
        event_type: Optional[str],
        event_data: Dict[str, Any] | list[Dict[str, Any]] | None = None,
        linked_message_id: str | None = None,
    ):
        """Send an event message to a specific session"""
        event_message = create_event_message(
            self._session_id, channel, event, event_type, event_data, linked_message_id
        )
        await self.send(event_message)
        if self._debug:
            logger.debug(f"Sent event message: {event_message.to_dict()}")

    async def send_error(
        self,
        channel: Optional[str],
        error: str,
        linked_message_id: str | None = None,
    ):
        """Send an error message to a specific session"""
        error_message = create_error_message(
            session_id=self._session_id,
            channel=channel if channel is not None else str(uuid.uuid4()),
            error_message=error,
            linked_message_id=linked_message_id,
        )

        await self.send(error_message)
        if self._debug:
            logger.debug(f"Sent error message: {error_message.to_dict()}")

    async def send_exception(
        self,
        e: Exception,
        linked_message_id: str | None = None,
        message: Message | None = None,
        channel: Optional[str] = None,
    ):
        """Send an error message to a specific session"""
        if message is not None:
            error_message = create_error_message_from_message(
                message, error_message=str(e), linked_message_id=linked_message_id
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

    def enable_compression(self, enabled: bool = True) -> None:
        """Enable or disable compression for all messages.

        Args:
            enabled: Whether to enable compression
        """
        self._compression_enabled = enabled
        logger.info(
            f"Message compression {'enabled' if enabled else 'disabled'} for session {self._session_id}"
        )

    def set_compression_level(self, level: int) -> None:
        """Set the compression level (0-9, where 9 is maximum compression).

        Args:
            level: Compression level from 0 (no compression) to 9 (maximum)
        """
        if not 0 <= level <= 9:
            raise ValueError("Compression level must be between 0 and 9")

        self._compression_level = level
        logger.info(f"Compression level set to {level} for session {self._session_id}")

    def set_compression_threshold(self, threshold: int) -> None:
        """Set the minimum message size in bytes for compression to be applied.

        Args:
            threshold: Size threshold in bytes
        """
        if threshold < 0:
            raise ValueError("Compression threshold must be a positive number")

        self._compression_threshold = threshold
        logger.info(
            f"Compression threshold set to {threshold} bytes for session {self._session_id}"
        )

    def set_polling_interval(self, interval: float) -> None:
        """Set the polling interval for the message processor.

        Args:
            interval: Polling interval in seconds
        """
        if interval <= 0:
            raise ValueError("Polling interval must be greater than zero")

        self._polling_interval = interval
        logger.info(
            f"Message polling interval set to {interval} seconds for session {self._session_id}"
        )

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
