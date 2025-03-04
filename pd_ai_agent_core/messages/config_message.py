from pd_ai_agent_core.messages.message import Message
from pd_ai_agent_core.core_types.content_message import ContentMessage
from typing import Any, Optional, Dict
from pd_ai_agent_core.common.constants import CONFIG_SUBJECT
from pd_ai_agent_core.common.constants import GLOBAL_CHANNEL


class ConfigMessage(ContentMessage):
    def __init__(self, key: str, value: Any):
        self.content = {"key": key, "value": value}

    def copy(self) -> "ConfigMessage":
        return ConfigMessage(
            key=self.content["key"],
            value=self.content["value"],
        )

    def subject(self) -> str:
        return CONFIG_SUBJECT

    def get(self, key: Optional[str] = None) -> Any:
        if key is None:
            return self.content
        return self.content.get(key)

    def to_dict(self) -> Dict[str, Any]:
        return {"key": self.content["key"], "value": self.content["value"]}


def create_config_message(
    session_id: str,
    channel: Optional[str],
    key: str,
    value: Any,
    linked_message_id: Optional[str] = None,
    is_partial: bool = False,
) -> Message:
    msg = Message(
        session_id=session_id,
        channel=channel if channel is not None else GLOBAL_CHANNEL,
        subject=CONFIG_SUBJECT,
        body=ConfigMessage(key, value),
    )
    msg.linked_message_id = linked_message_id
    msg.is_partial = is_partial
    return msg
