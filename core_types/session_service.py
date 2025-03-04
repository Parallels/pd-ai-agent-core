from abc import ABC, abstractmethod


class SessionService(ABC):
    def __init__(self, session_id: str):
        self.session_id = session_id

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def register(self) -> None:
        pass

    @abstractmethod
    def unregister(self) -> None:
        pass
