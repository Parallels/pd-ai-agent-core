import json
from typing import List, Callable, Union, Optional, Any, Dict
from pd_ai_agent_core.common.defaults import DEFAULT_MODEL
from pd_ai_agent_core.helpers.strings import normalize_string

# Third-party imports
from pydantic import BaseModel, HttpUrl
from enum import Enum

AgentFunction = Callable[[], Union[str, "LlmChatAgent", dict]]


class AttachmentType(Enum):
    """Enum representing different types of attachments that can be used in agent messages."""

    TEXT = "text"
    IMAGE = "image"
    CODEBLOCK = "codeblock"
    FILE = "file"
    AUDIO = "audio"
    VIDEO = "video"

    def __str__(self) -> str:
        return self.value


class AttachmentContextVariable(BaseModel):
    name: str
    id: str
    type: AttachmentType = AttachmentType.TEXT
    value: str
    download_url: Optional[str] = None
    language: Optional[str] = None
    format: Optional[str] = None

    def to_dict(self):
        return {
            "name": self.name,
            "id": self.id,
            "type": str(
                self.type
            ),  # Convert enum to string to make it JSON serializable
            "value": self.value,
            "download_url": self.download_url,
            "language": self.language,
            "format": self.format,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data["name"],
            id=data["id"],
            type=AttachmentType(data["type"]),
            value=data["value"],
            download_url=data["download_url"],
            language=data["language"],
            format=data["format"],
        )


class DataResult:
    value: Any
    context_variables: Dict[str, Any] = dict()


class LlmChatAgentResponseAction(BaseModel):
    id: str
    name: str
    description: str
    type: str
    value: str
    parameters: dict
    icon: Optional[str] = None
    group_id: Optional[str] = None

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "value": self.value,
            "parameters": self.parameters,
            "icon": self.icon,
            "group_id": self.group_id,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            type=data["type"],
            value=data["value"],
            parameters=data["parameters"],
            icon=data["icon"],
            group_id=data["group_id"],
        )


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
        args: Optional[Dict[str, Any]] = None,
        env: Optional[Dict[str, Any]] = None,
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
        self.args = args
        self.env = env


class LlmChatResponse(BaseModel):
    messages: List = []
    agent: Optional[LlmChatAgent] = None
    context_variables: dict = {}
    actions: List[LlmChatAgentResponseAction] = []
    attachments: List[AttachmentContextVariable] = []

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
    actions: List[LlmChatAgentResponseAction] = []
    attachments: List[AttachmentContextVariable] = []

    def __init__(
        self,
        status: str,
        message: str,
        error: Optional[str] = None,
        data: Optional[Union[dict, List[dict]]] = None,
        agent: Optional[LlmChatAgent] = None,
        context_variables: dict = {},
        actions: List[LlmChatAgentResponseAction] = [],
        attachments: List[AttachmentContextVariable] = [],
    ):
        self.status = status
        self.message = message
        self.error = error
        self.data = data
        self.agent = agent
        self.context_variables = context_variables
        self.actions = actions
        self.attachments = attachments

    def to_dict(self):
        return {
            "status": self.status,
            "message": self.message,
            "error": self.error,
            "data": self.data if self.data is not None else None,
            "actions": [action.to_dict() for action in self.actions],
            "attachments": [attachment.to_dict() for attachment in self.attachments],
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
            actions=[
                LlmChatAgentResponseAction.from_dict(action)
                for action in data["actions"]
            ],
            attachments=[
                AttachmentContextVariable.from_dict(attachment)
                for attachment in data["attachments"]
            ],
        )
