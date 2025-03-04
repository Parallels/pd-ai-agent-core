from typing import Dict, Any, Optional, List
from datetime import datetime
from websockets.server import WebSocketServerProtocol
from pd_ai_agent_core.core_types.session_channel import SessionChannel, ChannelStatus
from pd_ai_agent_core.common.constants import GLOBAL_CHANNEL


class Session:
    GLOBAL_CHANNEL_ID = GLOBAL_CHANNEL

    def __init__(self, session_id: str):
        self.id = session_id
        self.created_at = datetime.now()
        self.last_active = datetime.now()
        self._channels: Dict[str, SessionChannel] = {}
        self.debug: bool = False
        self._websocket: Optional[WebSocketServerProtocol] = None
        # Create global channel
        self._channels[self.GLOBAL_CHANNEL_ID] = SessionChannel(
            self.GLOBAL_CHANNEL_ID, is_global=True
        )

    def set_websocket(self, websocket: WebSocketServerProtocol) -> None:
        self._websocket = websocket

    def websocket(self) -> Optional[WebSocketServerProtocol]:
        return self._websocket

    def get_or_create_channel(self, channel_id: str) -> SessionChannel:
        """Get existing channel or create new one"""
        if channel_id not in self._channels:
            self._channels[channel_id] = SessionChannel(channel_id)
        return self._channels[channel_id]

    def get_global_channel(self) -> SessionChannel:
        """Get the global channel"""
        return self._channels[self.GLOBAL_CHANNEL_ID]

    def close_channel(self, channel_id: str) -> bool:
        """Close a specific channel"""
        if channel_id == self.GLOBAL_CHANNEL_ID:
            return False  # Can't close global channel
        if channel_id in self._channels:
            self._channels[channel_id].close()
            return True
        return False

    def archive_channel(self, channel_id: str) -> bool:
        """Archive a specific channel"""
        if channel_id == self.GLOBAL_CHANNEL_ID:
            return False  # Can't archive global channel
        if channel_id in self._channels:
            self._channels[channel_id].archive()
            return True
        return False

    def get_active_channels(self) -> List[SessionChannel]:
        """Get all active channels"""
        return [
            channel
            for channel in self._channels.values()
            if channel.status == ChannelStatus.ACTIVE
        ]

    def broadcast_to_channels(self, message: Dict[str, Any]) -> None:
        """Broadcast message to all active channels"""
        for channel in self.get_active_channels():
            channel.add_message(message)
