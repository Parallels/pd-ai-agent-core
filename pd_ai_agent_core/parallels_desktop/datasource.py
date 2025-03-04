from typing import Dict, List, Optional, ClassVar
import logging
from pd_ai_agent_core.parallels_desktop.models.virtual_machine import VirtualMachine
from datetime import datetime, timedelta
from pd_ai_agent_core.parallels_desktop.get_vms_from_prlctl import get_vms_from_prlctl
from pd_ai_agent_core.parallels_desktop.vm_parser import parse_vm_json

logger = logging.getLogger(__name__)


class VirtualMachineDataSource:
    """Singleton class to manage VirtualMachine data source"""

    _instance: ClassVar[Optional["VirtualMachineDataSource"]] = None

    @classmethod
    def initialize(cls) -> None:
        """Initialize the singleton instance"""
        if cls._instance is None:
            cls._instance = cls()

    @classmethod
    def get_instance(cls) -> "VirtualMachineDataSource":
        """Get the singleton instance"""
        if cls._instance is None:
            raise RuntimeError("VirtualMachineDataSource not initialized")
        return cls._instance

    def __init__(self):
        if self._instance is not None:
            raise RuntimeError("Use get_instance() to access VirtualMachineDataSource")

        self._vms: Dict[str, VirtualMachine] = {}  # vm_id -> VM
        self._last_update: Optional[datetime] = None
        self._cache_duration = timedelta(seconds=300)  # cache for 5 minutes
        vms = get_vms_from_prlctl()
        if vms.success:
            for vm in vms.raw_result:
                vm_model = parse_vm_json(vm)
                self._vms[vm_model.id] = vm_model

    def update_vm(self, vm: VirtualMachine) -> None:
        """Update a single VM in the cache"""
        self._vms[vm.id] = vm
        self._last_update = datetime.now()

    def update_vm_state(self, vm_id: str, state: str) -> None:
        """Update the state of a VM in the cache"""
        self._vms[vm_id].state = state
        self._last_update = datetime.now()

    def update_vms(self, vms: List[VirtualMachine]) -> None:
        """Update multiple VMs in the cache"""
        for vm in vms:
            self._vms[vm.id] = vm
        self._last_update = datetime.now()

    def get_vm(self, vm_id: str) -> Optional[VirtualMachine]:
        """Get a VirtualMachine by ID"""
        return self._vms.get(vm_id)

    def get_all_vms(self) -> List[VirtualMachine]:
        """Get all VMs"""
        return list(self._vms.values())

    def get_vms_by_state(self, state: str) -> List[VirtualMachine]:
        """Get all VMs in a specific state"""
        return [vm for vm in self._vms.values() if vm.state.lower() == state.lower()]

    def get_running_vms_count(self) -> int:
        """Get count of running VMs"""
        return len(self.get_vms_by_state("running"))

    def is_cache_valid(self) -> bool:
        """Check if the cache is still valid"""
        if self._last_update is None:
            return False
        return datetime.now() - self._last_update < self._cache_duration

    def clear_cache(self) -> None:
        """Clear the cache"""
        self._vms.clear()
        self._last_update = None

    def remove_vm(self, vm_id: str) -> None:
        """Remove a VM from the cache"""
        self._vms.pop(vm_id, None)

    def get_vms_by_name_pattern(self, pattern: str) -> List[VirtualMachine]:
        """Get VMs matching a name pattern"""
        return [vm for vm in self._vms.values() if pattern.lower() in vm.name.lower()]

    def get_vms_stats(self) -> Dict[str, int]:
        """Get VM statistics by state"""
        stats = {}
        for vm in self._vms.values():
            state = vm.state.lower()
            stats[state] = stats.get(state, 0) + 1
        return stats

    def length(self) -> int:
        """Get the number of VMs in the cache"""
        return len(self._vms)
