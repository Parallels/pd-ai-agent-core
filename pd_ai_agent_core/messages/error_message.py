from pd_ai_agent_core.core_types.content_message import ContentMessage
from pd_ai_agent_core.messages.message import Message
import uuid
from typing import Optional
from pd_ai_agent_core.common.constants import ERROR_SUBJECT
from pd_ai_agent_core.common.message_status import MessageStatus


class ErrorMessage(ContentMessage):
    def __init__(
        self,
        error_message: str,
        error_type: Optional[str] = None,
        traceback: Optional[str] = None,
    ):
        self._subject = ERROR_SUBJECT
        self._content = {
            "error_message": error_message,
            "error_type": error_type,
            "traceback": traceback,
        }

    def copy(self) -> "ErrorMessage":
        return ErrorMessage(
            error_message=self._content["error_message"],
            error_type=self._content["error_type"],
            traceback=self._content["traceback"],
        )

    def subject(self) -> str:
        return self._subject

    def to_dict(self) -> dict:
        return {
            "error_message": self._content["error_message"],
            "error_type": self._content["error_type"],
            "traceback": self._content["traceback"],
        }

    def get(self, key: str) -> str:
        return self._content[key]


def create_error_message(
    session_id: str,
    channel: Optional[str],
    error_message: str,
    linked_message_id: Optional[str] = None,
    is_partial: bool = False,
) -> Message:
    msg = Message(
        session_id=session_id,
        channel=channel if channel is not None else str(uuid.uuid4()),
        subject=ERROR_SUBJECT,
        body=ErrorMessage(error_message),
    )
    msg.is_complete = True
    msg.status = MessageStatus.COMPLETE
    msg.linked_message_id = linked_message_id
    msg.is_partial = is_partial
    return msg


def create_error_message_from_message(
    message: Message,
    error_message: str,
    error_type: Optional[str] = None,
    traceback: Optional[str] = None,
    linked_message_id: Optional[str] = None,
    is_partial: bool = False,
) -> Message:
    """Create error message from existing message"""
    msg = Message(
        session_id=message.session_id,
        channel=message.channel,
        subject="error",
        context=message.context,
        body=ErrorMessage(error_message, error_type, traceback),
    )
    msg.sender = message.sender
    msg.status = message.status
    msg.message_id = message.message_id
    msg.tool_calls = message.tool_calls
    msg._is_complete = message._is_complete
    msg.linked_message_id = linked_message_id
    msg.is_partial = is_partial
    return msg
