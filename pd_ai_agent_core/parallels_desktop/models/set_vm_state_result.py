from pydantic import BaseModel
from enum import Enum


class SetVmStateResult(BaseModel):
    success: bool
    message: str
    exit_code: int
    error: str
    vm: dict

    def to_dict(self) -> dict:
        return self.model_dump()


class VirtualMachineState(Enum):
    UNKNOWN = "unknown"
    START = "start"
    STOP = "stop"
    SUSPEND = "suspend"
    RESUME = "resume"
    PAUSE = "pause"
    SHUTDOWN = "shutdown"
    RESTART = "reboot"
