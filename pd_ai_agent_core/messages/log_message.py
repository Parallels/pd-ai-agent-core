from datetime import datetime
from typing import Optional
from pd_ai_agent_core.core_types.content_message import ContentMessage
from pd_ai_agent_core.common.constants import LOG_SUBJECT, GLOBAL_CHANNEL
from enum import Enum
from pd_ai_agent_core.common.message_status import MessageStatus
from pd_ai_agent_core.messages.message import Message
import uuid


class LogLevel(Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    TRACE = "trace"
    CRITICAL = "critical"


class LogMessage(ContentMessage):
    def __init__(
        self, session_id: str, channel: str, level: LogLevel, log_message: str
    ):
        self.timestamp = datetime.now().isoformat()
        self.session_id = session_id
        self.channel = channel
        self.level = level
        self.log_message = log_message

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "session_id": self.session_id,
            "channel": self.channel,
            "level": self.level.value,
            "log_message": self.log_message,
        }

    def copy(self) -> "LogMessage":
        return LogMessage(
            session_id=self.session_id,
            channel=self.channel,
            level=self.level,
            log_message=self.log_message,
        )

    def subject(self) -> str:
        return LOG_SUBJECT

    def get(self, key: str) -> str:
        return self.to_dict()[key]


def create_log_message(
    session_id: str,
    channel: Optional[str],
    level: LogLevel,
    log_message: str,
    linked_message_id: Optional[str] = None,
    is_partial: bool = False,
) -> Message:
    msg = Message(
        session_id=session_id,
        channel=channel if channel is not None else str(uuid.uuid4()),
        subject=LOG_SUBJECT,
        body=LogMessage(session_id, channel or GLOBAL_CHANNEL, level, log_message),
    )
    msg.is_complete = True
    msg.status = MessageStatus.COMPLETE
    msg.linked_message_id = linked_message_id
    msg.is_partial = is_partial
    return msg
