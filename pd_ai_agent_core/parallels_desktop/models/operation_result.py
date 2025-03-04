from pydantic import BaseModel


class OperationResult(BaseModel):
    success: bool
    message: str
    exit_code: int
    error: str

    def to_dict(self) -> dict:
        return self.model_dump()
