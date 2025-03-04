from pd_ai_agent_core.messages.message import Message
from pd_ai_agent_core.core_types.content_message import ContentMessage
from typing import Dict, Any, Optional
import uuid
from pd_ai_agent_core.common.constants import (
    CHAT_SUBJECT,
    TOOL_CHANGE_SUBJECT,
    AGENT_FUNCTION_CALL_SUBJECT,
    GLOBAL_CHANNEL,
)
from pd_ai_agent_core.common.message_status import MessageStatus


class StreamChatMessage(ContentMessage):
    def __init__(self, sender: str, role: str, content: str):
        self.sender = sender
        self.role = role
        self.content = content
        self.msg_type = "chat_stream"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sender": self.sender,
            "role": self.role,
            "content": self.content,
            "msg_type": self.msg_type,
        }

    def copy(self) -> "StreamChatMessage":
        return StreamChatMessage(self.sender, self.role, self.content)

    def subject(self) -> str:
        return CHAT_SUBJECT

    def get(self, key: Optional[str] = None) -> Any:
        if key == "content":
            return self.content
        if key == "sender":
            return self.sender
        if key == "role":
            return self.role
        if key == "msg_type":
            return self.msg_type
        return None


class ToolChangeChatMessage(ContentMessage):
    def __init__(self, name: str, arguments: Dict[str, Any]):
        self.name = name
        self.arguments = arguments
        self.msg_type = "tool_change"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "arguments": self.arguments,
            "msg_type": self.msg_type,
        }

    def copy(self) -> "ToolChangeChatMessage":
        return ToolChangeChatMessage(self.name, self.arguments)

    def subject(self) -> str:
        return TOOL_CHANGE_SUBJECT

    def get(self, key: Optional[str] = None) -> Any:
        if key == "name":
            return self.name
        if key == "arguments":
            return self.arguments
        if key == "msg_type":
            return self.msg_type
        if self.arguments is not None:
            for key in self.arguments:
                if key == key:
                    return self.arguments[key]
        return None


class AgentFunctionCallChatMessage(ContentMessage):
    def __init__(self, name: str, arguments: Dict[str, Any]):
        self.name = name
        self.arguments = arguments
        self.msg_type = "agent_function_call"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "arguments": self.arguments,
            "msg_type": self.msg_type,
        }

    def copy(self) -> "AgentFunctionCallChatMessage":
        return AgentFunctionCallChatMessage(self.name, self.arguments)

    def subject(self) -> str:
        return AGENT_FUNCTION_CALL_SUBJECT

    def get(self, key: Optional[str] = None) -> Any:
        if key == "name":
            return self.name
        if key == "arguments":
            return self.arguments
        if key == "msg_type":
            return self.msg_type
        if self.arguments is not None:
            for key in self.arguments:
                if key == key:
                    return self.arguments[key]
        return None


def create_stream_chat_message(
    session_id: str,
    channel: Optional[str],
    sender: str,
    role: str,
    content: str,
    is_complete: bool,
    linked_message_id: Optional[str] = None,
    is_partial: bool = False,
) -> Message:
    msg = Message(
        session_id=session_id,
        channel=channel if channel is not None else GLOBAL_CHANNEL,
        subject=CHAT_SUBJECT,
        body=StreamChatMessage(
            sender=sender,
            role=role,
            content=content,
        ),
    )
    msg.is_complete = is_complete
    msg.message_id = str(uuid.uuid4())
    if is_complete:
        msg.status = MessageStatus.COMPLETE
    else:
        msg.status = MessageStatus.STREAMING
    msg.linked_message_id = linked_message_id
    msg.is_partial = is_partial
    return msg


def create_tool_change_chat_message(
    session_id: str,
    channel: Optional[str],
    name: str,
    arguments: Dict[str, Any],
    linked_message_id: Optional[str] = None,
    is_partial: bool = False,
) -> Message:
    msg = Message(
        session_id=session_id,
        channel=channel if channel is not None else GLOBAL_CHANNEL,
        subject=TOOL_CHANGE_SUBJECT,
        body=ToolChangeChatMessage(
            name=name,
            arguments=arguments,
        ),
    )
    msg.is_complete = False
    msg.message_id = str(uuid.uuid4())
    msg.linked_message_id = linked_message_id
    msg.is_partial = is_partial
    return msg


def create_agent_function_call_chat_message(
    session_id: str,
    channel: Optional[str],
    name: str,
    arguments: Dict[str, Any] = {},
    linked_message_id: Optional[str] = None,
    is_partial: bool = False,
) -> Message:
    msg = Message(
        session_id=session_id,
        channel=channel if channel is not None else GLOBAL_CHANNEL,
        subject=AGENT_FUNCTION_CALL_SUBJECT,
        body=AgentFunctionCallChatMessage(
            name=name,
            arguments=arguments,
        ),
    )
    msg.is_complete = False
    msg.linked_message_id = linked_message_id
    msg.is_partial = is_partial
    msg.message_id = str(uuid.uuid4())
    return msg


def create_clean_agent_function_call_chat_message(
    session_id: str,
    channel: Optional[str],
    linked_message_id: Optional[str] = None,
    is_partial: bool = False,
) -> Message:
    msg = Message(
        session_id=session_id,
        channel=channel if channel is not None else GLOBAL_CHANNEL,
        subject=AGENT_FUNCTION_CALL_SUBJECT,
        body=AgentFunctionCallChatMessage(
            name="",
            arguments={},
        ),
    )
    msg.is_complete = False
    msg.linked_message_id = linked_message_id
    msg.is_partial = is_partial
    msg.message_id = str(uuid.uuid4())
    return msg
