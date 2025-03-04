from typing import Dict, Optional, Type, cast, TypeVar
from pd_ai_agent_core.core_types.session_service import SessionService
import logging

logger = logging.getLogger(__name__)

T = TypeVar("T", bound="SessionService")


class Service:
    def __init__(self, session_id: str):
        self._session_id = session_id
        self._services: Dict[str, SessionService] = {}

    def register(self, name: str, service: SessionService) -> bool:
        """
        Register a service instance for this session
        Returns True if service was registered, False if it already existed
        """
        if name in self._services:
            existing_service = self._services[name]
            if isinstance(existing_service, type(service)):
                logger.warning(
                    f"Service '{name}' of type {type(service)} already registered for session '{self._session_id}'"
                )
                return False

        self._services[name] = service
        return True

    def unregister(self) -> None:
        """Unregister all services for this session"""
        for service in list(self._services.values()):
            if hasattr(service, "unregister"):
                service.unregister()

    def get(self, name: str) -> Optional[SessionService]:
        """Get a service instance for this session"""
        return self._services.get(name)


class ServiceRegistry:
    _sessions: Dict[str, Service] = {}

    @classmethod
    def get_session(cls, session_id: str) -> Service:
        """Get or create a Service instance for the session"""
        if session_id not in cls._sessions:
            cls._sessions[session_id] = Service(session_id)
        return cls._sessions[session_id]

    @classmethod
    def register(cls, session_id: str, name: str, service: SessionService) -> bool:
        """
        Register a service instance for a specific session
        Returns True if service was registered, False if it already existed
        """
        session = cls.get_session(session_id)
        return session.register(name, service)

    @classmethod
    def get(cls, session_id: str, name: str, service_type: Type[T]) -> T:
        """Get a service instance for a specific session

        Example usage:
            # Get notification service for a session
            notification_service = ServiceRegistry.get(session_id, "notification")
            notification_service.send_message("Hello")

            # Get log service for a session
            log_service = ServiceRegistry.get(session_id, "log")
            log_service.info(session_id, "channel", "Log message")

            # Get config service for a session
            config_service = ServiceRegistry.get(session_id, "config")
            config_service.get("some.config.key")
        """
        session = cls.get_session(session_id)
        service = session.get(name)
        if service is None:
            raise ValueError(f"Service '{name}' not found for session '{session_id}'")
        if not isinstance(service, service_type):
            raise ValueError(f"Service '{name}' is not of type {service_type}")
        return cast(service_type, service)

    @classmethod
    def unregister_service(cls, session_id: str, name: str) -> bool:
        """
        Unregister a specific service from a session
        Returns True if service was unregistered, False if it didn't exist
        """
        if session_id not in cls._sessions:
            return False

        session = cls._sessions[session_id]
        service = session.get(name)
        if service is None:
            return False

        # Call service's unregister method if it exists
        if hasattr(service, "unregister"):
            service.unregister()

        # Remove the service from the session
        session._services.pop(name, None)
        return True

    @classmethod
    def cleanup_session(cls, session_id: str) -> None:
        """
        Remove all services for a session and clean up the session itself
        """
        if session_id not in cls._sessions:
            return

        # Get all services for cleanup
        session = cls._sessions[session_id]
        services = list(session._services.items())

        # Clean up each service
        for name, service in services:
            # Call service's unregister method if it exists
            if hasattr(service, "unregister"):
                service.unregister()
            cls.unregister_service(session_id, name)

        # Remove the session
        cls._sessions.pop(session_id, None)
