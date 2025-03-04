from dataclasses import dataclass
from typing import Any, Dict
from pd_ai_agent_core.core_types.content_message import ContentMessage
from pd_ai_agent_core.common.constants import SYSTEM_MESSAGE_SUBJECT
from pd_ai_agent_core.messages.message import Message
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class SystemMessageStatus(Enum):
    STARTED = "started"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    SKIPPED = "skipped"
    PENDING = "pending"


@dataclass
class SystemMessage(ContentMessage):
    status: SystemMessageStatus
    link_id: str
    error: str
    message: str
    data: Dict[str, Any]

    def __init__(
        self,
        status: SystemMessageStatus,
        link_id: str,
        error: str,
        message: str,
        data: Dict[str, Any],
    ):
        self.status = status
        self.link_id = link_id
        self.error = error
        self.message = message
        self.data = data

    def subject(self) -> str:
        return SYSTEM_MESSAGE_SUBJECT

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status.value,
            "link_id": self.link_id,
            "error": self.error,
            "message": self.message,
            "data": self.data,
        }

    def get(self, key: str) -> Any:
        return self.data.get(key)

    def copy(self) -> "SystemMessage":
        return SystemMessage(
            self.status, self.link_id, self.error, self.message, self.data
        )

    @staticmethod
    def from_dict(data: ContentMessage | dict[str, Any]) -> "SystemMessage | None":
        """Create a BackgroundMessage from a dictionary, returns None if invalid"""
        if isinstance(data, ContentMessage):
            data = data.to_dict()

        try:
            if not isinstance(data, dict):
                return None

            status = data.get("status")
            link_id = data.get("link_id")
            error = data.get("error")
            message = data.get("message")
            message_data = data.get("data", {})

            if not status:
                return None

            if status.upper() not in SystemMessageStatus.__members__:
                return None

            result = SystemMessage(
                status=SystemMessageStatus(status),
                link_id=link_id if link_id else "",
                error=error if error else "",
                message=message if message else "",
                data=message_data if message_data else {},
            )
            return result
        except Exception as e:
            logger.error(f"Error creating SystemMessage from dict: {e}")
            return None


def create_system_message(
    status: SystemMessageStatus,
    link_id: str,
    error: str,
    message: str,
    data: Dict[str, Any],
) -> SystemMessage:
    return SystemMessage(status, link_id, error, message, data)


def create_system_message_from_message(
    status: SystemMessageStatus,
    message: Message,
) -> Message:
    msg = Message(
        session_id=message.session_id,
        channel=message.channel,
        subject=SYSTEM_MESSAGE_SUBJECT,
        body=SystemMessage(
            status=status,
            link_id=message.message_id,
            error="",
            message="",
            data={},
        ).to_dict(),
    )
    msg.is_complete = message.is_complete
    msg.status = message.status
    msg.linked_message_id = message.linked_message_id
    msg.is_partial = message.is_partial
    return msg
