from pydantic import BaseModel
from .vm import VM


class GetVmResult(BaseModel):
    success: bool
    message: str
    exit_code: int
    error: str
    raw_result: dict
    vm: VM

    def to_dict(self) -> dict:
        return self.model_dump()
