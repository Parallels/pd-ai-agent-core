from pydantic import BaseModel


class CloneVmResult(BaseModel):
    success: bool
    message: str
    exit_code: int
    error: str
