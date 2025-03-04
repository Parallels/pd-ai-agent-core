from typing import Dict, Optional, ClassVar
from datetime import datetime, timedelta
from pd_ai_agent_core.core_types.session import Session


class SessionManager:
    _instance: ClassVar[Optional["SessionManager"]] = None

    @classmethod
    def initialize(cls, debug: bool = False) -> None:
        """Initialize the singleton instance"""
        if cls._instance is None:
            cls._instance = cls(debug)

    @classmethod
    def get_instance(cls) -> "SessionManager":
        """Get the singleton instance"""
        if cls._instance is None:
            raise RuntimeError("SessionManager not initialized")
        return cls._instance

    def __init__(self, debug: bool = False):
        if self._instance is not None:
            raise RuntimeError("Use get_instance() to access SessionManager")
        self.sessions: Dict[str, Session] = {}
        self.debug = debug

    def is_session_valid(self, session_id: str) -> bool:
        """Check if a session is valid and active"""
        return session_id in self.sessions

    def create_session(self, session_id: str) -> Session:
        """Create a new session"""
        if session_id in self.sessions:
            return self.sessions[session_id]

        session = Session(session_id)
        self.sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[Session]:
        """Get session by ID"""
        return self.sessions.get(session_id)

    def delete_session(self, session_id: str) -> None:
        """Delete a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]

    def cleanup_inactive(self, max_age_minutes: int = 30) -> None:
        """Remove inactive sessions"""
        cutoff = datetime.now() - timedelta(minutes=max_age_minutes)
        to_delete = [
            sid
            for sid, session in self.sessions.items()
            if session.last_active < cutoff
        ]
        for sid in to_delete:
            self.delete_session(sid)

    @property
    def active_sessions(self) -> int:
        """Get count of active sessions"""
        return len(self.sessions)
