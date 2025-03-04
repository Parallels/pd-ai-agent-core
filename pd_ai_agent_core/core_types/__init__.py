# Import and expose key modules
from .content_message import ContentMessage
from .background_agent import BackgroundAgent
from .llm_chat_ai_agent import LlmChatAgent, AgentFunction
from .session import Session
from .session_channel import SessionChannel
from .session_context import SessionContext
from .session_service import SessionService
from .session_type import SessionType

# Also expose the parallels_chat_ai_agent module for backward compatibility
from .llm_chat_ai_agent import LlmChatAgent as ParallelsLlmChatAgent
from .llm_chat_ai_agent import AgentFunction as ParallelsAgentFunction

__all__ = [
    "ContentMessage",
    "BackgroundAgent",
    "LlmChatAgent",
    "AgentFunction",
    "Session",
    "SessionChannel",
    "SessionContext",
    "SessionService",
    "SessionType",
    "ParallelsLlmChatAgent",
    "ParallelsAgentFunction",
]
