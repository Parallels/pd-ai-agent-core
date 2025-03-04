from pydantic import BaseModel


class GetVmOsVersionResult(BaseModel):
    success: bool
    message: str
    exit_code: int
    error: str
