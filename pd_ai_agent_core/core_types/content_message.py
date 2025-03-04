from abc import ABC, abstractmethod
from typing import Any, Optional, Dict


class ContentMessage(ABC):
    @abstractmethod
    def subject(self) -> str:
        """Get the subject of the message"""
        pass

    @abstractmethod
    def copy(self) -> "ContentMessage":
        """Create a copy of the message"""
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary format"""
        pass

    @abstractmethod
    def get(self, key: Optional[str] = None) -> Any:
        """Get value from message content"""
        pass
