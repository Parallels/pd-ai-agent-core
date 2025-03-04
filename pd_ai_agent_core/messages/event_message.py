from pd_ai_agent_core.core_types.content_message import ContentMessage
from typing import Any, Dict, Optional
from pd_ai_agent_core.messages.message import Message
from pd_ai_agent_core.common.constants import EVENT_SUBJECT, GLOBAL_CHANNEL


class EventMessage(ContentMessage):
    def __init__(
        self,
        event_name: str,
        event_type: Optional[str],
        event_data: Dict[str, Any] | list[Dict[str, Any]] | None,
    ):
        self._subject = EVENT_SUBJECT
        self._content = {
            "event_name": event_name,
            "event_type": event_type,
            "event_data": event_data,
        }

    def copy(self) -> "EventMessage":
        return EventMessage(
            event_name=self._content["event_name"],
            event_type=self._content["event_type"],
            event_data=self._content["event_data"],
        )

    def subject(self) -> str:
        return self._subject

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_name": self._content["event_name"],
            "event_type": self._content["event_type"],
            "event_data": self._content["event_data"],
        }

    def get(self, key: Optional[str] = None) -> Any:
        if "event_data" in self._content:
            if isinstance(self._content["event_data"], list):
                return (
                    [item[key] for item in self._content["event_data"]]
                    if key is not None
                    else self._content["event_data"]
                )
            else:
                return (
                    self._content["event_data"][key]
                    if key is not None
                    else self._content["event_data"]
                )
        return self._content[key] if key is not None else self._content


def create_event_message(
    session_id: str,
    channel: Optional[str],
    event_name: str,
    event_type: Optional[str],
    event_data: Dict[str, Any] | list[Dict[str, Any]] | None = None,
    linked_message_id: Optional[str] = None,
    is_partial: bool = False,
) -> Message:
    msg = Message(
        session_id=session_id,
        channel=channel if channel is not None else GLOBAL_CHANNEL,
        subject=EVENT_SUBJECT,
        body=EventMessage(event_name, event_type, event_data),
    )
    msg.linked_message_id = linked_message_id
    msg.is_partial = is_partial
    return msg
