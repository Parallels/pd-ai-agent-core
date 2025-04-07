from pd_ai_agent_core.messages.message import Message
from pd_ai_agent_core.core_types.content_message import ContentMessage
from typing import Dict, Any, Optional, List
import uuid
from pd_ai_agent_core.common.constants import (
    CHAT_SUBJECT,
    TOOL_CHANGE_SUBJECT,
    AGENT_FUNCTION_CALL_SUBJECT,
    GLOBAL_CHANNEL,
)
from pd_ai_agent_core.common.message_status import MessageStatus
from pydantic import BaseModel
from pd_ai_agent_core.core_types.llm_chat_ai_agent import AttachmentContextVariable


class StreamChatMessageAction(BaseModel):
    id: str
    name: str
    description: str
    type: str
    value: str
    parameters: dict
    icon: Optional[str] = None
    group_id: Optional[str] = None

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "value": self.value,
            "parameters": self.parameters,
            "icon": self.icon,
            "group_id": self.group_id,
        }


class StreamChatMessage(ContentMessage):
    def __init__(
        self,
        sender: str,
        role: str,
        content: str,
        actions: List[StreamChatMessageAction] = [],
        icon: Optional[str] = None,
        attachments: List[AttachmentContextVariable] = [],
    ):
        self.sender = sender
        self.role = role
        self.content = content
        self.msg_type = "chat_stream"
        self.icon = icon
        self.actions = actions
        self.attachments = attachments

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sender": self.sender,
            "role": self.role,
            "content": self.content,
            "msg_type": self.msg_type,
            "actions": [action.to_dict() for action in self.actions],
            "icon": self.icon,
            "attachments": [attachment.to_dict() for attachment in self.attachments],
        }

    def copy(self) -> "StreamChatMessage":
        return StreamChatMessage(
            self.sender, self.role, self.content, self.actions, self.icon
        )

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
        if key == "icon":
            return self.icon
        if key == "actions":
            return self.actions
        return None


class ToolChangeChatMessage(ContentMessage):
    def __init__(
        self, name: str, arguments: Dict[str, Any], icon: Optional[str] = None
    ):
        self.name = name
        self.arguments = arguments
        self.msg_type = "tool_change"
        self.icon = icon

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "arguments": self.arguments,
            "msg_type": self.msg_type,
            "icon": self.icon,
        }

    def copy(self) -> "ToolChangeChatMessage":
        return ToolChangeChatMessage(self.name, self.arguments, self.icon)

    def subject(self) -> str:
        return TOOL_CHANGE_SUBJECT

    def get(self, key: Optional[str] = None) -> Any:
        if key == "name":
            return self.name
        if key == "arguments":
            return self.arguments
        if key == "msg_type":
            return self.msg_type
        if key == "icon":
            return self.icon
        if self.arguments is not None:
            for key in self.arguments:
                if key == key:
                    return self.arguments[key]
        return None


class AgentFunctionCallChatMessage(ContentMessage):
    def __init__(
        self, name: str, arguments: Dict[str, Any], icon: Optional[str] = None
    ):
        self.name = name
        self.arguments = arguments
        self.msg_type = "agent_function_call"
        self.icon = icon

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "arguments": self.arguments,
            "msg_type": self.msg_type,
            "icon": self.icon,
        }

    def copy(self) -> "AgentFunctionCallChatMessage":
        return AgentFunctionCallChatMessage(self.name, self.arguments, self.icon)

    def subject(self) -> str:
        return AGENT_FUNCTION_CALL_SUBJECT

    def get(self, key: Optional[str] = None) -> Any:
        if key == "name":
            return self.name
        if key == "arguments":
            return self.arguments
        if key == "msg_type":
            return self.msg_type
        if key == "icon":
            return self.icon
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
    actions: List[StreamChatMessageAction] = [],
    icon: Optional[str] = None,
) -> Message:
    msg = Message(
        session_id=session_id,
        channel=channel if channel is not None else GLOBAL_CHANNEL,
        subject=CHAT_SUBJECT,
        icon=icon,
        body=StreamChatMessage(
            sender=sender,
            role=role,
            content=content,
            actions=actions,
            icon=icon,
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
    icon: Optional[str] = None,
) -> Message:
    msg = Message(
        session_id=session_id,
        channel=channel if channel is not None else GLOBAL_CHANNEL,
        subject=TOOL_CHANGE_SUBJECT,
        icon=icon,
        body=ToolChangeChatMessage(
            name=name,
            arguments=arguments,
            icon=icon,
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
    icon: Optional[str] = None,
) -> Message:
    msg = Message(
        session_id=session_id,
        channel=channel if channel is not None else GLOBAL_CHANNEL,
        subject=AGENT_FUNCTION_CALL_SUBJECT,
        icon=icon,
        body=AgentFunctionCallChatMessage(
            name=name,
            arguments=arguments,
            icon=icon,
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
