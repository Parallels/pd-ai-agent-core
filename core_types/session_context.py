class SessionContext:
    def __init__(
        self,
        session_id: str,
        channel: str,
        message_id: str,
        subject: str,
        debug: bool,
        linked_message_id: str | None = None,
        is_partial: bool = False,
    ):
        self.session_id = session_id
        self.channel = channel
        self.message_id = message_id
        self.linked_message_id = linked_message_id
        self.is_partial = is_partial
        self.subject = subject
        self.debug = debug

    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "channel": self.channel,
            "message_id": self.message_id,
            "linked_message_id": self.linked_message_id,
            "is_partial": self.is_partial,
            "subject": self.subject,
            "debug": self.debug,
        }
