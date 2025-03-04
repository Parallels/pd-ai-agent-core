from pydantic import BaseModel
from pd_ai_agent_core.parallels_desktop.models.virtual_machine import VirtualMachine


class GetVmResult(BaseModel):
    success: bool
    message: str
    exit_code: int
    error: str
    raw_result: dict
    vm: VirtualMachine

    class Config:
        arbitrary_types_allowed = True

    def to_dict(self) -> dict:
        return self.model_dump()
