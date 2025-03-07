from pd_ai_agent_core.parallels_desktop.get_vms import get_vm
from pd_ai_agent_core.parallels_desktop.helpers import get_prlctl_command
from typing import List
import subprocess
from pd_ai_agent_core.parallels_desktop.models.delete_vm_result import DeleteVmResult


def delete_vm(vm_id: str) -> DeleteVmResult:
    """Delete a VM.
    Args:
        vm_id (str): The ID of the VM to delete.
    Returns:
        bool: True if the VM was deleted successfully, False otherwise.
    """
    if not vm_id:
        raise ValueError("VM ID is required")
    try:
        vmResult = get_vm(vm_id)
        if not vmResult.success:
            return DeleteVmResult(
                success=False,
                message=vmResult.message,
                exit_code=vmResult.exit_code,
                error=vmResult.error,
            )
        if vmResult.vm.state == "running":
            return DeleteVmResult(
                success=False,
                message="VM is running",
                exit_code=1,
                error="VM is running",
            )
        cmd: List[str] = [get_prlctl_command(), "delete", vm_id]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
            shell=False,
        )
        if result.returncode == 0:
            return DeleteVmResult(
                success=True,
                message="VM deleted successfully",
                exit_code=result.returncode,
                error="",
            )
        else:
            return DeleteVmResult(
                success=False,
                message="Failed to delete VM",
                exit_code=result.returncode,
                error=result.stderr,
            )
    except Exception as e:
        return DeleteVmResult(
            success=False,
            message=f"Failed to delete VM: {e}",
            exit_code=1,
            error=str(e),
        )
