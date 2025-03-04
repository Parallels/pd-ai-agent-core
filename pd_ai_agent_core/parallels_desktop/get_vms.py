from pd_ai_agent_core.parallels_desktop.get_vm_screenshot import get_vm_screenshot
from pd_ai_agent_core.parallels_desktop.models.get_vm_result import GetVmResult
from pd_ai_agent_core.parallels_desktop.datasource import VirtualMachineDataSource


def get_vms(take_screenshot: bool = False) -> GetVmResult:
    datasource = VirtualMachineDataSource.get_instance()
    vms = datasource.get_all_vms()
    if take_screenshot:
        for vm in vms:
            vm_screenshot_result = get_vm_screenshot(vm.id)
            vm.screenshot = vm_screenshot_result.screenshot
            datasource.update_vm(vm)

    return GetVmResult(
        success=True, message="VMs listed successfully", exit_code=0, error="", vms=vms
    )


def get_vm(vm_id: str, take_screenshot: bool = False) -> GetVmResult:
    datasource = VirtualMachineDataSource.get_instance()
    vm = datasource.get_vm(vm_id)
    if take_screenshot:
        vm_screenshot_result = get_vm_screenshot(vm.id)
        vm.screenshot = vm_screenshot_result.screenshot
        datasource.update_vm(vm)
    return GetVmResult(
        success=True, message="VM listed successfully", exit_code=0, error="", vm=vm
    )
