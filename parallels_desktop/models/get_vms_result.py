from pydantic import BaseModel
from .virtual_machine import VirtualMachine
from typing import List


class GetVmsResult(BaseModel):
    success: bool
    message: str
    exit_code: int
    error: str
    raw_result: List[dict]
    vms: List[VirtualMachine]

    class Config:
        arbitrary_types_allowed = True

    def to_dict(self) -> dict:
        return self.model_dump()
