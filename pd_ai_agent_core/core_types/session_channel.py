from typing import Dict, Any
from datetime import datetime
from pd_ai_agent_core.core_types.llm_chat_ai_agent import LlmChatAgent
from enum import Enum


class ChannelStatus(Enum):
    ACTIVE = "active"
    CLOSED = "closed"
    ARCHIVED = "archived"


class SessionChannel:
    def __init__(self, channel_id: str, is_global: bool = False):
        self.id = channel_id
        self.created_at = datetime.now()
        self.last_active = datetime.now()
        self._messages: list = []
        self._metadata: Dict[str, Any] = {}
        self._context_variables: Dict[str, Any] = {}
        self._session_context: Dict[str, Any] = {}
        self.agent: LlmChatAgent | None = None
        self.is_global: bool = is_global
        self.status: ChannelStatus = ChannelStatus.ACTIVE

    def add_message(self, message: Dict[str, Any]) -> None:
        self._messages.append(message)
        self.update_last_active()

    def messages(self) -> list:
        return self._messages

    def clear_messages(self) -> None:
        self._messages = []

    def update_metadata(self, key: str, value: Any) -> None:
        self._metadata[key] = value

    def set_metadata(self, data: Dict[str, Any]) -> None:
        self._metadata.update(data)

    def metadata(self) -> Dict[str, Any]:
        return self._metadata

    def update_context_variable(self, key: str, value: Any) -> None:
        self._context_variables[key] = value

    def set_context_variables(self, data: Dict[str, Any]) -> None:
        self._context_variables.update(data)

    def context_variables(self) -> Dict[str, Any]:
        return self._context_variables

    def update_session_context(self, key: str, value: Any) -> None:
        self._session_context[key] = value

    def set_session_context(self, data: Dict[str, Any]) -> None:
        self._session_context.update(data)

    def session_context(self) -> Dict[str, Any]:
        return self._session_context

    def update_last_active(self) -> None:
        self.last_active = datetime.now()

    def close(self) -> None:
        """Close the channel"""
        self.status = ChannelStatus.CLOSED

    def archive(self) -> None:
        """Archive the channel"""
        self.status = ChannelStatus.ARCHIVED

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "last_active": self.last_active.isoformat(),
            "is_global": self.is_global,
            "status": self.status.value,
            "metadata": self._metadata,
            "context_variables": self._context_variables,
        }

    # ... other methods similar to current Session class
