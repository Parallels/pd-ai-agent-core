from pd_ai_agent_core.parallels_desktop.get_vms import get_vm
from pd_ai_agent_core.parallels_desktop.helpers import get_prlctl_command
from typing import List
import subprocess
from pd_ai_agent_core.parallels_desktop.models.clone_vm_result import CloneVmResult


def clone_vm(vm_id: str, new_vm_name: str) -> CloneVmResult:
    """Clone a VM.
    Args:
        vm_id (str): The ID of the VM to clone.
        new_vm_name (str): The name of the new VM.
    Returns:
        bool: True if the VM was cloned successfully, False otherwise.
    """
    if not vm_id:
        raise ValueError("VM ID is required")
    if not new_vm_name:
        raise ValueError("New VM name is required")
    try:
        vmResult = get_vm(vm_id)
        if not vmResult.success:
            return CloneVmResult(
                success=False,
                message=vmResult.message,
                exit_code=vmResult.exit_code,
                error=vmResult.error,
            )
        if vmResult.vm.state != "running":
            return CloneVmResult(
                success=False,
                message="VM is not running",
                exit_code=1,
                error="VM is not running",
            )
        cmd: List[str] = [
            get_prlctl_command(),
            "clone",
            vm_id,
            "--name",
            new_vm_name,
            "--regenerate-src-uuid",
        ]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
            shell=False,
        )
        if result.returncode == 0:
            return CloneVmResult(
                success=True,
                message="VM cloned successfully",
                exit_code=0,
                error="",
            )
        else:
            return CloneVmResult(
                success=False,
                message="Failed to clone VM",
                exit_code=result.returncode,
                error=result.stderr,
            )
    except Exception as e:
        return CloneVmResult(
            success=False,
            message=f"Failed to clone VM: {e}",
            exit_code=1,
            error=str(e),
        )
