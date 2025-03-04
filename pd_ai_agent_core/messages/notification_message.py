from pd_ai_agent_core.core_types.content_message import ContentMessage
from pd_ai_agent_core.common.constants import NOTIFICATION_SUBJECT, GLOBAL_CHANNEL
from enum import Enum
from typing import Dict, Any, Optional
from pd_ai_agent_core.messages.message import Message
import uuid


class NotificationType(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"
    SECURITY = "security"
    LOG = "log"
    EVENT = "event"


class NotificationActionType(Enum):
    BACKGROUND_MESSAGE = "background_message"
    LINK = "link"
    URL = "url"


class NotificationAction:
    def __init__(
        self,
        label: str,
        value: str,
        icon: str,
        kind: NotificationActionType,
        data: Dict[str, Any],
    ):
        self._id = uuid.uuid4()
        self.label = label
        self.value = value
        self.icon = icon
        self.kind = kind
        self.data = data

    def to_dict(self) -> Dict[str, Any]:
        return {
            "label": self.label,
            "value": self.value,
            "icon": self.icon,
            "kind": self.kind.value,
            "data": self.data,
        }


class NotificationMessage(ContentMessage):
    def __init__(
        self,
        message: str,
        type: NotificationType,
        replace: bool = False,
        data: Dict[str, Any] | list[Dict[str, Any]] | None = None,
        actions: list[NotificationAction] = [],
        details: str | None = None,
    ):
        self._subject = NOTIFICATION_SUBJECT
        self._content = {
            "message": message,
            "type": type.value,
            "replace": replace,
            "data": data,
            "actions": actions,
            "details": details,
        }

    def copy(self) -> "NotificationMessage":
        return NotificationMessage(
            message=self._content["message"],
            type=NotificationType(self._content["type"]),
            data=self._content["data"],
            details=self._content["details"],
        )

    def subject(self) -> str:
        return self._subject

    def to_dict(self) -> Dict[str, Any]:
        if "actions" in self._content:
            actions = [action.to_dict() for action in self._content["actions"]]
        else:
            actions = []
        result = {
            "message": self._content["message"],
            "type": self._content["type"],
            "data": self._content["data"],
            "actions": actions,
            "details": self._content["details"],
            "replace": self._content["replace"],
        }
        return result

    def get(self, key: Optional[str] = None) -> Any:
        if "data" in self._content:
            if isinstance(self._content["data"], list):
                return (
                    [item[key] for item in self._content["data"]]
                    if key is not None
                    else self._content["data"]
                )
            else:
                return (
                    self._content["data"][key]
                    if key is not None
                    else self._content["data"]
                )
        return None

    def actions(self) -> list[NotificationAction]:
        return self._content["actions"]

    def action(self, key: str) -> NotificationAction | None:
        return next(
            (action for action in self._content["actions"] if action.label == key),
            None,
        )

    def add_action(self, action: NotificationAction):
        self._content["actions"].append(action)

    def remove_action(self, key: str):
        self._content["actions"] = [
            action for action in self._content["actions"] if action.label != key
        ]


def create_notification_message(
    session_id: str,
    channel: Optional[str],
    message: str,
    type: NotificationType,
    replace: bool = False,
    data: Dict[str, Any] | list[Dict[str, Any]] | None = None,
    actions: list[NotificationAction] | None = None,
    details: str | None = None,
    linked_message_id: Optional[str] = None,
    is_partial: bool = False,
) -> Message:
    msg = Message(
        session_id=session_id,
        channel=channel if channel is not None else GLOBAL_CHANNEL,
        subject=NOTIFICATION_SUBJECT,
        body=NotificationMessage(
            message=message,
            type=type,
            data=data,
            actions=actions or [],
            details=details,
            replace=replace,
        ),
    )
    msg.linked_message_id = linked_message_id
    msg.is_partial = is_partial
    return msg


def create_info_notification_message(
    session_id: str,
    channel: Optional[str],
    message: str,
    details: str | None = None,
    data: Dict[str, Any] | list[Dict[str, Any]] | None = None,
    actions: list[NotificationAction] | None = None,
    replace: bool = False,
    linked_message_id: Optional[str] = None,
    is_partial: bool = False,
) -> Message:
    msg = create_notification_message(
        session_id,
        channel,
        message,
        NotificationType.INFO,
        replace,
        data,
        actions,
        details,
        linked_message_id,
        is_partial,
    )
    return msg


def create_warning_notification_message(
    session_id: str,
    channel: Optional[str],
    message: str,
    details: str | None = None,
    data: Dict[str, Any] | list[Dict[str, Any]] | None = None,
    actions: list[NotificationAction] | None = None,
    replace: bool = False,
    linked_message_id: Optional[str] = None,
    is_partial: bool = False,
) -> Message:
    msg = create_notification_message(
        session_id,
        channel,
        message,
        NotificationType.WARNING,
        replace,
        data,
        actions,
        details,
        linked_message_id,
        is_partial,
    )
    return msg


def create_error_notification_message(
    session_id: str,
    channel: Optional[str],
    message: str,
    details: str | None = None,
    data: Dict[str, Any] | list[Dict[str, Any]] | None = None,
    actions: list[NotificationAction] | None = None,
    replace: bool = False,
    linked_message_id: Optional[str] = None,
    is_partial: bool = False,
) -> Message:
    msg = create_notification_message(
        session_id,
        channel,
        message,
        NotificationType.ERROR,
        replace,
        data,
        actions,
        details,
        linked_message_id,
        is_partial,
    )
    return msg


def create_success_notification_message(
    session_id: str,
    channel: Optional[str],
    message: str,
    details: str | None = None,
    replace: bool = False,
    data: Dict[str, Any] | list[Dict[str, Any]] | None = None,
    actions: list[NotificationAction] | None = None,
    linked_message_id: Optional[str] = None,
    is_partial: bool = False,
) -> Message:
    msg = create_notification_message(
        session_id,
        channel,
        message,
        NotificationType.SUCCESS,
        replace,
        data,
        actions,
        details,
        linked_message_id,
        is_partial,
    )
    return msg
