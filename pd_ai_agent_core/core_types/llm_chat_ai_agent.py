import json
from typing import List, Callable, Union, Optional, Any, Dict
from pd_ai_agent_core.common.defaults import DEFAULT_MODEL
from pd_ai_agent_core.helpers.strings import normalize_string

# Third-party imports
from pydantic import BaseModel, HttpUrl

AgentFunction = Callable[[], Union[str, "LlmChatAgent", dict]]


class DataResult:
    value: Any
    context_variables: Dict[str, Any] = dict()


class AgentFunctionDescriptor:
    name: str
    description: str

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def get_string(self) -> str:
        return f"{normalize_string(self.name)}::{self.description}"


class LlmChatAgent:
    def __init__(
        self,
        name: str,
        instructions: Union[str, Callable[[Dict[str, Any]], str]],
        description: Optional[str] = None,
        model: str = DEFAULT_MODEL,
        functions: List[AgentFunction] = [],
        function_descriptions: List[AgentFunctionDescriptor] = [],
        parallel_tool_calls: bool = True,
        transfer_instructions: Optional[str] = None,
        icon: Optional[Union[str, HttpUrl]] = None,
        tool_choice: Optional[str] = None,
    ):
        self.id = normalize_string(name)
        self.name = name
        self.description = description
        self.instructions = instructions
        self.model = model
        self.functions = functions or []
        self.function_descriptions = function_descriptions or []
        self.parallel_tool_calls = parallel_tool_calls
        self.transfer_instructions = transfer_instructions
        self.icon = icon
        self.tool_choice = tool_choice


class LlmChatResponse(BaseModel):
    messages: List = []
    agent: Optional[LlmChatAgent] = None
    context_variables: dict = {}

    class Config:
        arbitrary_types_allowed = True


class LlmChatResult(BaseModel):
    """
    Encapsulates the possible return values for an agent function.

    Attributes:
        value (str): The result value as a string.
        agent (Dict): The agent instance as a dictionary.
        context_variables (dict): A dictionary of context variables.
    """

    value: str = ""
    agent: Optional[LlmChatAgent] = None
    context_variables: dict = {}

    class Config:
        arbitrary_types_allowed = True


class LlmChatAgentResponse:
    status: str
    message: str
    error: Optional[str] = None
    data: Optional[Union[dict, List[dict]]] = None
    agent: Optional[LlmChatAgent] = None
    context_variables: dict = {}

    def __init__(
        self,
        status: str,
        message: str,
        error: Optional[str] = None,
        data: Optional[Union[dict, List[dict]]] = None,
        agent: Optional[LlmChatAgent] = None,
        context_variables: dict = {},
    ):
        self.status = status
        self.message = message
        self.error = error
        self.data = data
        self.agent = agent
        self.context_variables = context_variables

    def to_dict(self):
        return {
            "status": self.status,
            "message": self.message,
            "error": self.error,
            "data": self.data if self.data is not None else None,
        }

    def value(self) -> str:
        if self.data is not None:
            return json.dumps(self.data)
        if self.error:
            return self.error
        if self.message:
            return self.message
        return self.status

    @staticmethod
    def from_dict(data: dict):
        return LlmChatAgentResponse(
            status=data["status"],
            message=data["message"],
            error=data["error"],
            data=data["data"],
        )
