from pd_ai_agent_core.parallels_desktop.get_vm_screenshot import get_vm_screenshot
from pd_ai_agent_core.parallels_desktop.models.get_vm_result import GetVmResult
from pd_ai_agent_core.parallels_desktop.models.get_vms_result import GetVmsResult
from pd_ai_agent_core.parallels_desktop.datasource import VirtualMachineDataSource


def get_vms(take_screenshot: bool = False) -> GetVmResult:
    datasource = VirtualMachineDataSource.get_instance()
    vms = datasource.get_all_vms()
    if take_screenshot:
        for vm in vms:
            vm_screenshot_result = get_vm_screenshot(vm.id)
            vm.screenshot = vm_screenshot_result.screenshot or ""
            datasource.update_vm(vm)
    updated_vms = datasource.get_all_vms()
    updated_vms_dict = [vm.to_dict() for vm in updated_vms]
    return GetVmsResult(
        success=True,
        message="VMs listed successfully",
        exit_code=0,
        error="",
        raw_result=updated_vms_dict,
        vms=updated_vms,
    )


def get_vm(vm_id: str, take_screenshot: bool = False) -> GetVmResult:
    datasource = VirtualMachineDataSource.get_instance()
    vm = datasource.get_vm(vm_id)
    if vm is None:
        return GetVmResult(
            success=False,
            message="VM not found",
            exit_code=1,
            error="VM not found",
            vm=None,
        )
    if take_screenshot:
        vm_screenshot_result = get_vm_screenshot(vm.id)
        vm.screenshot = vm_screenshot_result.screenshot or ""
        datasource.update_vm(vm)
    updated_vm = datasource.get_vm(vm_id)
    if updated_vm is None:
        return GetVmResult(
            success=False,
            message="VM not found",
            exit_code=1,
            error="VM not found",
            vm=None,
        )
    updated_vm_dict = updated_vm.to_dict()
    return GetVmResult(
        success=True,
        message="VM listed successfully",
        exit_code=0,
        error="",
        raw_result=updated_vm_dict,
        vm=updated_vm,
    )
