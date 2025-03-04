from pd_ai_agent_core.core_types.content_message import ContentMessage
from typing import Any, Dict, Optional
from pd_ai_agent_core.messages.message import Message
from pd_ai_agent_core.common.constants import COMMAND_SUBJECT, GLOBAL_CHANNEL


class CommandMessage(ContentMessage):
    def __init__(
        self,
        command: str,
        args: Dict[str, Any],
        result: Optional[Any] = None,
        error: Optional[Any] = None,
        exit_code: Optional[int] = None,
        stdout: Optional[str] = None,
        stderr: Optional[str] = None,
    ):
        self._subject = COMMAND_SUBJECT
        self._content = {
            "command": command,
            "args": args,
            "result": result,
            "error": error,
            "exit_code": exit_code,
            "stdout": stdout,
            "stderr": stderr,
        }

    def copy(self) -> "CommandMessage":
        return CommandMessage(
            command=self._content["command"],
            args=self._content["args"],
            result=self._content["result"],
            error=self._content["error"],
            exit_code=self._content["exit_code"],
            stdout=self._content["stdout"],
            stderr=self._content["stderr"],
        )

    def subject(self) -> str:
        return self._subject

    def to_dict(self) -> Dict[str, Any]:
        return {
            "command": self._content["command"],
            "args": self._content["args"],
            "result": self._content["result"],
            "error": self._content["error"],
            "exit_code": self._content["exit_code"],
            "stdout": self._content["stdout"],
            "stderr": self._content["stderr"],
        }

    def get(self, key: Optional[str] = None) -> Any:
        if key is None:
            return self._content
        if key in self._content:
            return self._content[key]
        if "args" in self._content:
            return (
                self._content["args"][key] if key is not None else self._content["args"]
            )
        return None

    def command(self) -> str:
        return self._content["command"]

    def args(self) -> Dict[str, Any]:
        return self._content["args"]

    def result(self) -> Optional[Any]:
        return self._content["result"]

    def error(self) -> Optional[Any]:
        return self._content["error"]

    def exit_code(self) -> Optional[int]:
        return self._content["exit_code"]

    def stdout(self) -> Optional[str]:
        return self._content["stdout"]

    def stderr(self) -> Optional[str]:
        return self._content["stderr"]


def create_command_message(
    session_id: str,
    channel: Optional[str],
    command: str,
    result: Optional[Any] = None,
    error: Optional[Any] = None,
    exit_code: Optional[int] = None,
    stdout: Optional[str] = None,
    stderr: Optional[str] = None,
    args: Dict[str, Any] = {},
    linked_message_id: Optional[str] = None,
    is_partial: bool = False,
) -> Message:
    msg = Message(
        session_id=session_id,
        channel=channel if channel is not None else GLOBAL_CHANNEL,
        subject=COMMAND_SUBJECT,
        body=CommandMessage(
            command,
            args,
            result,
            error,
            exit_code,
            stdout,
            stderr,
        ),
    )
    msg.linked_message_id = linked_message_id
    msg.is_partial = is_partial
    return msg
