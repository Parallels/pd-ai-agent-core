from pydantic import BaseModel


class ExecuteVmCommandResult(BaseModel):
    output: str = ""
    error: str = ""
    exit_code: int = 0

    def to_dict(self):
        return {"output": self.output, "error": self.error, "exit_code": self.exit_code}

    @staticmethod
    def from_dict(data: dict):
        return ExecuteVmCommandResult(
            output=data.get("output", ""),
            error=data.get("error", ""),
            exit_code=data.get("exit_code", 0),
        )
