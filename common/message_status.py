from enum import Enum


class MessageStatus(Enum):
    WAITING = "waiting"
    COMPLETE = "complete"
    STREAMING = "streaming"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"
    TRACE = "trace"
    CRITICAL = "critical"
