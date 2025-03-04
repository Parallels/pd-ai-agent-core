from typing import Optional
from pd_ai_agent_core.common.constants import (
    NOTIFICATION_SERVICE_NAME,
    LOGGER_SERVICE_NAME,
)
from pd_ai_agent_core.messages.log_message import create_log_message, LogLevel
import uuid
import logging
from pd_ai_agent_core.helpers.strings import get_error_from_exception
from pd_ai_agent_core.services.service_registry import ServiceRegistry
from pd_ai_agent_core.services.notification_service import NotificationService
from pd_ai_agent_core.core_types.session_service import SessionService
import os
from pd_ai_agent_core.helpers.strings import parse_boolean

logger = logging.getLogger(__name__)


class LogService(SessionService):

    def __init__(self, session_id: str, debug: bool = False):
        self._debug = debug
        self._session_id = session_id
        ns = ServiceRegistry.get(
            session_id, NOTIFICATION_SERVICE_NAME, NotificationService
        )
        if ns is None:
            raise ValueError(f"Notification service not found for session {session_id}")
        self._ns = ns
        self._loop = None
        self._enable_ws_logging = False
        if os.getenv("PD_AI_DEBUG__SEND_WS_LOG") is not None:
            self._enable_ws_logging = parse_boolean(
                os.getenv("PD_AI_DEBUG__SEND_WS_LOG") or "false"
            )
        self.register()

    def name(self) -> str:
        return LOGGER_SERVICE_NAME

    def register(self) -> None:
        """Register this service with the registry"""
        if not ServiceRegistry.register(self._session_id, LOGGER_SERVICE_NAME, self):
            logger.info(
                f"Logger service already registered for session {self._session_id}"
            )
            return

    def unregister(self) -> None:
        """Unregister this service from the registry"""
        logger.info(f"Logger service unregistered for session {self._session_id}")

    def info(self, channel: Optional[str], message: str) -> None:
        log_message = create_log_message(
            session_id=self._session_id,
            channel=channel if channel else str(uuid.uuid4()),
            level=LogLevel.INFO,
            log_message=message,
        )
        logger.info(f"[{self._session_id}] [{channel}] {message}")
        if self._enable_ws_logging:
            self._ns.send_sync(log_message)

    def debug(self, channel: Optional[str], message: str) -> None:
        """Synchronous version of debug logging"""
        if not self._debug:
            return
        log_message = create_log_message(
            session_id=self._session_id,
            channel=channel if channel else str(uuid.uuid4()),
            level=LogLevel.DEBUG,
            log_message=message,
        )
        logger.debug(f"[{self._session_id}] [{channel}] {message}")
        if self._enable_ws_logging:
            self._ns.send_sync(log_message)

    def warning(self, channel: Optional[str], message: str) -> None:
        """Synchronous version of warning logging"""
        log_message = create_log_message(
            session_id=self._session_id,
            channel=channel if channel else str(uuid.uuid4()),
            level=LogLevel.WARNING,
            log_message=message,
        )
        logger.warning(f"[{self._session_id}] [{channel}] {message}")
        if self._enable_ws_logging:
            self._ns.send_sync(log_message)

    def error(self, channel: Optional[str], message: str) -> None:
        """Synchronous version of error logging"""

        log_message = create_log_message(
            session_id=self._session_id,
            channel=channel if channel else str(uuid.uuid4()),
            level=LogLevel.ERROR,
            log_message=message,
        )
        logger.error(f"[{self._session_id}] [{channel}] {message}")
        if self._enable_ws_logging:
            self._ns.send_sync(log_message)

    def exception(self, channel: Optional[str], message: str, e: Exception) -> None:
        """Synchronous version of error logging"""
        error_message = get_error_from_exception(message, e)
        log_message = create_log_message(
            session_id=self._session_id,
            channel=channel if channel else str(uuid.uuid4()),
            level=LogLevel.ERROR,
            log_message=f"{error_message['error_message']}: {error_message['error_type']}",
        )
        logger.error(f"[{self._session_id}] [{channel}] {message}")
        if self._enable_ws_logging:
            self._ns.send_sync(log_message)

    def trace(self, channel: Optional[str], message: str) -> None:
        """Synchronous version of trace logging"""
        log_message = create_log_message(
            session_id=self._session_id,
            channel=channel if channel else str(uuid.uuid4()),
            level=LogLevel.TRACE,
            log_message=message,
        )
        logger.debug(f"[{self._session_id}] [{channel}] {message}")
        if self._enable_ws_logging:
            self._ns.send_sync(log_message)
