from dataclasses import dataclass
from typing import Any, Dict
from datetime import datetime
from pd_ai_agent_core.core_types.content_message import ContentMessage
from pd_ai_agent_core.common.constants import BACKGROUND_MESSAGE_SUBJECT


@dataclass
class BackgroundMessage(ContentMessage):
    message_type: str  # Supports wildcards like "vm.*"
    data: Dict[str, Any]
    timestamp: datetime = datetime.now()
    retry_count: int = 0
    max_retries: int = 10

    def __init__(self, message_type: str, data: Dict[str, Any]):
        self.message_type = message_type
        self.data = data
        self.timestamp = datetime.now()
        self.retry_count = 0
        self.max_retries = 10

    def subject(self) -> str:
        return BACKGROUND_MESSAGE_SUBJECT

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_type": self.message_type,
            "data": self.data,
        }

    def get(self, key: str) -> Any:
        return self.data.get(key)

    def copy(self) -> "BackgroundMessage":
        return BackgroundMessage(self.message_type, self.data)

    @staticmethod
    def from_dict(data: ContentMessage | dict[str, Any]) -> "BackgroundMessage | None":
        """Create a BackgroundMessage from a dictionary, returns None if invalid"""
        if isinstance(data, ContentMessage):
            data = data.to_dict()

        try:
            if not isinstance(data, dict):
                return None

            message_type = data.get("message_type")
            message_data = data.get("data", {})

            if not message_type or not isinstance(message_type, str):
                return None

            result = BackgroundMessage(
                message_type=message_type,
                data=message_data,
            )
            return result
        except Exception:
            return None


def create_background_message(
    message_type: str, data: Dict[str, Any]
) -> BackgroundMessage:
    return BackgroundMessage(message_type, data)
