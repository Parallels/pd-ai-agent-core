from typing import Optional, Any
from pd_ai_agent_core.core_types.content_message import ContentMessage
import uuid
from pd_ai_agent_core.common.constants import ERROR_SUBJECT
from pd_ai_agent_core.common.message_status import MessageStatus


class Message:
    def __init__(
        self,
        session_id: str,
        channel: str = "",
        subject: str = "",
        body: ContentMessage | dict = {},
        context: Optional[dict] = None,
    ):
        self.session_id = session_id
        self.channel = channel
        self.subject = subject
        self.body = body
        self.context = context
        self._is_complete = False
        self.message_id = str(uuid.uuid4())
        self.sender = None
        self.error = None
        self.status = None
        self._linked_message_id = None
        self._is_partial = False
        self._partial_index = -1
        self.tool_calls = None

    @property
    def is_chat(self) -> bool:
        """Check if message is a chat type"""
        return self.subject == "chat"

    @property
    def is_command(self) -> bool:
        """Check if message is a command type"""
        return self.subject == "command"

    @property
    def is_complete(self) -> bool:
        """Check if message processing is complete"""
        return self._is_complete

    @is_complete.setter
    def is_complete(self, value: bool) -> None:
        """Set message completion status"""
        self._is_complete = value

    @property
    def linked_message_id(self) -> Optional[str]:
        """Get linked message ID"""
        return self._linked_message_id

    @linked_message_id.setter
    def linked_message_id(self, value: Optional[str]) -> None:
        """Set linked message ID"""
        self._linked_message_id = value

    @property
    def is_partial(self) -> bool:
        """Check if message is a partial message"""
        return self._is_partial

    @is_partial.setter
    def is_partial(self, value: bool) -> None:
        """Set partial message status"""
        self._is_partial = value

    @property
    def partial_index(self) -> int:
        """Get partial index"""
        return self._partial_index

    @partial_index.setter
    def partial_index(self, value: int) -> None:
        """Set partial index"""
        self._partial_index = value

    def increment_partial_index(self) -> None:
        """Increment partial index"""
        self._partial_index += 1

    def create_with_error(self, error_message: str) -> "Message":
        """Create a new message instance with error from existing message"""
        body_copy = (
            self.body.copy() if isinstance(self.body, dict) else self.body.copy()
        )
        new_message = Message(
            session_id=self.session_id,
            channel=self.channel,
            subject=ERROR_SUBJECT,
            body=body_copy,
            context=self.context.copy() if self.context else None,
        )
        new_message.is_complete = True
        new_message.message_id = self.message_id
        new_message.sender = self.sender
        new_message.error = error_message
        return new_message

    def mark_complete(self) -> None:
        """Mark message as complete"""
        self._is_complete = True

    def set_message_id(self, message_id: str) -> None:
        """Set message ID for tracking stream responses"""
        self.message_id = message_id

    def set_sender(self, sender: str) -> None:
        """Set message sender"""
        self.sender = sender

    def get_body(self, key: Optional[str] = None):
        """Get message body, optionally accessing nested key"""
        if isinstance(self.body, dict):
            if key is None:
                return self.body
            return self.body.get(key)
        # Handle IbodyMessage
        return self.body.get(key) if key is None else self.body.get(key)

    def get_context(self, key: Optional[str] = None):
        """Get message context, optionally accessing nested key"""
        if self.context is None:
            return None
        if key is None:
            return self.context
        return self.context.get(key)

    def set_status(self, status: MessageStatus) -> None:
        """Set message status"""
        self.status = status

    def get_status(self) -> Optional[MessageStatus]:
        """Get message status"""
        return self.status

    def set_tool_calls(self, tool_calls: list) -> None:
        """Set tool calls for message"""
        self.tool_calls = tool_calls

    def get_tool_calls(self) -> Optional[list]:
        """Get tool calls for message"""
        return self.tool_calls

    def to_dict(self) -> dict:
        """Convert message to dictionary format"""
        body_dict = (
            self.body.to_dict() if isinstance(self.body, ContentMessage) else self.body
        )
        return {
            "session_id": self.session_id,
            "channel": self.channel,
            "message_id": self.message_id,
            "subject": self.subject,
            "body": body_dict,
            "is_complete": self.is_complete,
            "sender": self.sender,
            "error": self.error,
            "context": self.context,
            "status": self.status.value if self.status else None,
            "tool_calls": self.tool_calls,
            "linked_message_id": self.linked_message_id,
            "is_partial": self.is_partial,
            "partial_index": self.partial_index,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Message":
        """Create message instance from dictionary"""
        status = data.get("status")
        msg = cls(
            session_id=data["session_id"],
            channel=data["channel"],
            subject=data["subject"],
            body=data["body"],
        )
        msg.context = data.get("context")

        msg.error = data.get("error")
        msg.is_complete = data.get("is_complete", False)
        msg.message_id = data.get("message_id")
        msg.sender = data.get("sender")
        msg.status = MessageStatus(status) if status else None
        msg.tool_calls = data.get("tool_calls")
        msg.linked_message_id = data.get("linked_message_id")
        msg.is_partial = data.get("is_partial", False)
        msg.partial_index = data.get("partial_index", -1)
        return msg

    def copy(self) -> "Message":
        """Create a copy of the message"""
        body_copy = (
            self.body.copy() if isinstance(self.body, dict) else self.body.copy()
        )
        new_message = Message(
            session_id=self.session_id,
            channel=self.channel,
            subject=self.subject,
            body=body_copy,
            context=self.context.copy() if self.context else None,
        )
        new_message.is_complete = self.is_complete
        new_message.message_id = self.message_id
        new_message.sender = self.sender
        new_message.error = self.error
        new_message.status = self.status
        new_message.tool_calls = self.tool_calls
        new_message.linked_message_id = self.linked_message_id
        new_message.is_partial = self.is_partial
        new_message.partial_index = self.partial_index
        return new_message

    def get(self, key: Optional[str] = None) -> Any:
        """Get value from message body"""
        if isinstance(self.body, dict):
            if key is None:
                return self.body
            return self.body.get(key)
        return self.body.get(key) if key is None else self.body.get(key)
