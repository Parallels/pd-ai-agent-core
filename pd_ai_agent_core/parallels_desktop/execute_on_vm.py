import subprocess
from typing import List
from pd_ai_agent_core.parallels_desktop.get_vms import get_vm
from pd_ai_agent_core.parallels_desktop.helpers import get_prlctl_command
from pd_ai_agent_core.parallels_desktop.models.execute_vm_command_result import (
    ExecuteVmCommandResult,
)


def execute_on_vm(
    vm_id: str, command: str, args: List[str] = []
) -> ExecuteVmCommandResult:
    if not vm_id:
        return ExecuteVmCommandResult(error="No VM ID provided", exit_code=1)
    try:
        vm_details = get_vm(vm_id)
        if not vm_details.success:
            return ExecuteVmCommandResult(
                error=vm_details.message, exit_code=vm_details.exit_code
            )
        if vm_details.vm.state != "running":
            return ExecuteVmCommandResult(error="VM is not running", exit_code=1)
    except Exception as e:
        return ExecuteVmCommandResult(error=str(e), exit_code=1)
    try:
        cmdArgs = command.split(" ")
        if len(args) > 0:
            cmdArgs.extend(args)
        cmd: List[str] = [get_prlctl_command(), "exec", vm_id, *cmdArgs]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
            shell=False,
        )
        if result.returncode != 0:
            return ExecuteVmCommandResult(
                error=result.stderr, exit_code=result.returncode
            )
        return ExecuteVmCommandResult(output=result.stdout, exit_code=result.returncode)
    except subprocess.CalledProcessError as e:
        return ExecuteVmCommandResult(error=str(e), exit_code=1)
