from typing import Dict, Any


class PrlctlEventItem:
    timestamp: str
    vm_id: str
    event_name: str
    additional_info: Dict[str, str]

    def __init__(
        self,
        timestamp: str,
        vm_id: str,
        event_name: str,
        additional_info: Dict[str, str] = {},
    ) -> None:
        self.timestamp = timestamp
        self.vm_id = vm_id
        self.event_name = event_name
        self.additional_info = additional_info

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "vm_id": self.vm_id,
            "event_name": self.event_name,
            "additional_info": self.additional_info,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PrlctlEventItem":
        result = cls(
            timestamp=data["Timestamp"],
            vm_id=data["VM ID"],
            event_name=data["Event name"],
        )
        if "Additional info" in data:
            result.additional_info = data["Additional info"]
        return result
