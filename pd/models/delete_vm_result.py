from pydantic import BaseModel


class DeleteVmResult(BaseModel):
    success: bool
    message: str
    exit_code: int
    error: str
