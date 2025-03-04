import os
import sys

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import and expose key modules
# Use relative imports within the package
from .messages.message import Message
from .helpers import parse_boolean
from .core_types.content_message import ContentMessage
from .services.ocr_service import OCRService
from .services.service_registry import Service, ServiceRegistry
from .services.session_manager import SessionManager
from .core_types.llm_chat_ai_agent import LlmChatAgent, AgentFunction

# Import Parallels Desktop modules
from .parallels_desktop.models import *
from .parallels_desktop.get_vms import get_vms, get_vm
from .parallels_desktop.datasource import VirtualMachineDataSource

# Create an alias for backward compatibility
from .core_types.llm_chat_ai_agent import LlmChatAgent as ParallelsLlmChatAgent
from .core_types.llm_chat_ai_agent import AgentFunction as ParallelsAgentFunction

# Define what gets imported with "from pd_ai_agent_core import *"
__all__ = [
    "parse_boolean",
    "Message",
    "ContentMessage",
    "OCRService",
    "Service",
    "ServiceRegistry",
    "SessionManager",
    "LlmChatAgent",
    "AgentFunction",
    "ParallelsLlmChatAgent",
    "ParallelsAgentFunction",
    "get_vms",
    "get_vm",
    "VirtualMachineDataSource",
]
