import time
from pd_ai_agent_core.parallels_desktop.get_vms import get_vm
import subprocess
from typing import List
from pd_ai_agent_core.parallels_desktop.helpers import get_prlctl_command
from pd_ai_agent_core.parallels_desktop.models.set_vm_state_result import (
    SetVmStateResult,
    VirtualMachineState,
)


def set_vm_state(
    vm_id: str, state: VirtualMachineState, wait_for_completion: bool = False
) -> SetVmStateResult:
    """Set the state of a VM.
    Args:
        vm_id (str): The ID of the VM to set the state of.
        state (VMState): The state to set the VM to.
    Returns:
        bool: True if the state was set successfully, False otherwise.
    """
    if not vm_id:
        return SetVmStateResult(
            success=False,
            message="VM ID is required",
            exit_code=1,
            error="VM ID is required",
            vm={},
        )
    if state == VirtualMachineState.UNKNOWN:
        return SetVmStateResult(
            success=False,
            message="State is required",
            exit_code=1,
            error="State is required",
            vm={},
        )
    if not isinstance(state, VirtualMachineState):
        return SetVmStateResult(
            success=False,
            message="State must be a VirtualMachineState",
            exit_code=1,
            error="State must be a VirtualMachineState",
            vm={},
        )
    try:
        vmDetails = get_vm(vm_id=vm_id)
        if not vmDetails.success:
            return SetVmStateResult(
                success=False,
                message=vmDetails.message,
                exit_code=vmDetails.exit_code,
                error=vmDetails.error,
                vm={},
            )
        vmState = vmDetails.vm.state
        desired_state = state.value.lower()
        if vmState == "running":
            if state == VirtualMachineState.START:
                return SetVmStateResult(
                    success=True,
                    message="VM is already running",
                    exit_code=0,
                    error="",
                    vm=vmDetails.raw_result,
                )
            elif state == VirtualMachineState.RESUME:
                return SetVmStateResult(
                    success=True,
                    message="VM is already running",
                    exit_code=0,
                    error="",
                    vm=vmDetails.raw_result,
                )
        elif vmState == "stopped":
            if state == VirtualMachineState.STOP:
                return SetVmStateResult(
                    success=True,
                    message="VM is already stopped",
                    exit_code=0,
                    error="",
                    vm=vmDetails.raw_result,
                )
            elif state == VirtualMachineState.RESUME:
                return SetVmStateResult(
                    success=True,
                    message="VM is stopped, cannot resume",
                    exit_code=0,
                    error="",
                    vm=vmDetails.raw_result,
                )
            elif state == VirtualMachineState.PAUSE:
                return SetVmStateResult(
                    success=True,
                    message="VM is stopped, cannot pause",
                    exit_code=0,
                    error="",
                    vm=vmDetails.raw_result,
                )
            elif state == VirtualMachineState.SHUTDOWN:
                return SetVmStateResult(
                    success=True,
                    message="VM is stopped, cannot shutdown",
                    exit_code=0,
                    error="",
                    vm=vmDetails.raw_result,
                )
            elif state == VirtualMachineState.RESTART:
                return SetVmStateResult(
                    success=True,
                    message="VM is stopped, cannot reboot",
                    exit_code=0,
                    error="",
                    vm=vmDetails.raw_result,
                )
            elif state == VirtualMachineState.SUSPEND:
                return SetVmStateResult(
                    success=True,
                    message="VM is stopped, cannot suspend",
                    exit_code=0,
                    error="",
                    vm=vmDetails.raw_result,
                )
        elif vmState == "paused":
            if state == VirtualMachineState.PAUSE:
                return SetVmStateResult(
                    success=True,
                    message="VM is already paused",
                    exit_code=0,
                    error="",
                    vm=vmDetails.raw_result,
                )
            elif state == VirtualMachineState.SUSPEND:
                return SetVmStateResult(
                    success=True,
                    message="VM is already paused, cannot suspend",
                    exit_code=0,
                    error="",
                    vm=vmDetails.raw_result,
                )
        elif vmState == "suspended":
            if state == VirtualMachineState.PAUSE:
                return SetVmStateResult(
                    success=True,
                    message="VM is suspended, cannot pause",
                    exit_code=0,
                    error="",
                    vm=vmDetails.raw_result,
                )
            elif state == VirtualMachineState.SUSPEND:
                return SetVmStateResult(
                    success=True,
                    message="VM is already suspended",
                    exit_code=0,
                    error="",
                    vm=vmDetails.raw_result,
                )
        cmd: List[str] = [
            get_prlctl_command(),
            desired_state,
            vm_id,
        ]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
            shell=False,
        )
        if result.returncode != 0:
            return SetVmStateResult(
                success=False,
                message=result.stderr,
                exit_code=result.returncode,
                error=result.stderr,
                vm=vmDetails.vm,
            )
        # waiting for the vm to be ready
        if state == VirtualMachineState.START and wait_for_completion:
            waitFor = 30  # seconds
            while waitFor > 0:
                try:
                    cmd: List[str] = [
                        get_prlctl_command(),
                        "exec",
                        vm_id,
                        "echo",
                        "started",
                    ]
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        check=False,
                        shell=False,
                    )
                    if result.returncode == 0:
                        break
                except Exception:
                    pass
                time.sleep(1)
                waitFor -= 1
        vmDetails = get_vm(vm_id=vm_id)
        return SetVmStateResult(
            success=True,
            message="VM state set successfully",
            exit_code=0,
            error="",
            vm=vmDetails.raw_result,
        )
    except Exception as e:
        return SetVmStateResult(
            success=False,
            message=f"Error setting VM state: {e}",
            exit_code=1,
            error=str(e),
            vm={},
        )


def start_vm(vm_id: str, wait_for_completion: bool = False) -> SetVmStateResult:
    return set_vm_state(vm_id, VirtualMachineState.START, wait_for_completion)


def stop_vm(vm_id: str) -> SetVmStateResult:
    return set_vm_state(vm_id, VirtualMachineState.STOP)


def suspend_vm(vm_id: str) -> SetVmStateResult:
    return set_vm_state(vm_id, VirtualMachineState.SUSPEND)


def resume_vm(vm_id: str) -> SetVmStateResult:
    return set_vm_state(vm_id, VirtualMachineState.RESUME)


def pause_vm(vm_id: str) -> SetVmStateResult:
    return set_vm_state(vm_id, VirtualMachineState.PAUSE)


def shutdown_vm(vm_id: str) -> SetVmStateResult:
    return set_vm_state(vm_id, VirtualMachineState.SHUTDOWN)


def restart_vm(vm_id: str, wait_for_completion: bool = False) -> SetVmStateResult:
    stopOp = stop_vm(vm_id)
    if not stopOp.success:
        return stopOp
    startOp = start_vm(vm_id, wait_for_completion)
    if not startOp.success:
        return startOp
    return SetVmStateResult(
        success=True,
        message="VM restarted",
        exit_code=0,
        error="",
        vm=stopOp.vm,
    )
