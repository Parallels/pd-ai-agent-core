from pd_ai_agent_core.parallels_desktop.execute_on_vm import execute_on_vm
from pd_ai_agent_core.parallels_desktop.get_vms import get_vm
from pd_ai_agent_core.parallels_desktop.models.get_vm_os_version_result import (
    GetVmOsVersionResult,
)


def get_os_version(base_os: str, vm_id: str) -> GetVmOsVersionResult:
    if not vm_id:
        return GetVmOsVersionResult(
            success=False,
            message="No VM ID provided",
            exit_code=1,
            error="No VM ID provided",
        )
    if not base_os:
        return GetVmOsVersionResult(
            success=False,
            message="No base OS provided",
            exit_code=1,
            error="No base OS provided",
        )
    vmResult = get_vm(vm_id)
    if not vmResult.success:
        return GetVmOsVersionResult(
            success=False,
            message=vmResult.message,
            exit_code=vmResult.exit_code,
            error=vmResult.error,
        )
    if vmResult.vm.state != "running":
        return GetVmOsVersionResult(
            success=False,
            message="VM is not running",
            exit_code=1,
            error="VM is not running",
        )
    cmd = get_os_version_cmd(base_os)
    result = execute_on_vm(vm_id, cmd)
    if result.exit_code == 0:
        return GetVmOsVersionResult(
            success=True,
            message=result.output,
            exit_code=result.exit_code,
            error="",
        )
    else:
        return GetVmOsVersionResult(
            success=False,
            message="Failed to get OS version",
            exit_code=result.exit_code,
            error=result.error,
        )


def get_os_version_cmd(os: str) -> str:
    if os.lower() == "ubuntu":
        return "lsb_release -a"
    elif os.lower() == "debian":
        return "lsb_release -a"
    elif os.lower() == "macos" or os.lower() == "osx" or os.lower() == "darwin":
        return "sw_vers"
    elif os.lower() == "windows":
        return "ver"
    elif os.lower() == "fedora":
        return "lsb_release -a"
    else:
        return ""
