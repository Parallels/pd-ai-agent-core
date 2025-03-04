from pd_ai_agent_core.parallels_desktop.helpers import get_prlctl_command
from typing import List
import subprocess
import json
from pd_ai_agent_core.parallels_desktop.get_vm_screenshot import get_vm_screenshot
from pd_ai_agent_core.parallels_desktop.models.get_vm_result import GetVmResult
from pd_ai_agent_core.parallels_desktop.models.get_vms_result import GetVmsResult
from pd_ai_agent_core.parallels_desktop.vm_parser import parse_vm_json


def get_vms_from_prlctl(take_screenshot: bool = False) -> GetVmsResult:
    try:
        cmd: List[str] = [str(get_prlctl_command()), "list", "-a", "-i", "--json"]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            shell=False,
        )
        data = json.loads(result.stdout)
        if take_screenshot:
            for vm in data:
                vm_screenshot_result = get_vm_screenshot(vm["ID"])
                vm["Screenshot"] = vm_screenshot_result.screenshot
        return GetVmsResult(
            success=True,
            message="VMs listed successfully",
            exit_code=0,
            error="",
            raw_result=data,
            vms=[parse_vm_json(vm) for vm in data],
        )
    except subprocess.CalledProcessError as e:
        return GetVmsResult(
            success=False,
            message=f"Failed to list VMs: {e}",
            exit_code=1,
            error=str(e),
            raw_result=[],
            vms=[],
        )
    except json.JSONDecodeError as e:
        return GetVmsResult(
            success=False,
            message=f"Failed to parse VM list output: {e}",
            exit_code=1,
            error=str(e),
            raw_result=[],
            vms=[],
        )


def get_vm_from_prlctl(vm_id: str, take_screenshot: bool = False) -> GetVmResult:
    if not vm_id:
        raise RuntimeError("No VM ID provided")
    try:
        cmd: List[str] = [
            str(get_prlctl_command()),
            "list",
            vm_id,
            "-a",
            "-i",
            "--json",
        ]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            shell=False,
        )
        result = json.loads(result.stdout)
        if len(result) == 0:
            raise RuntimeError(f"VM {vm_id} not found")
        if take_screenshot:
            for vm in result:
                if vm["ID"] == vm_id:
                    vm_screenshot_result = get_vm_screenshot(vm_id)
                    vm["Screenshot"] = vm_screenshot_result.screenshot
        return GetVmResult(
            success=True,
            message=f"VM {vm_id} listed successfully",
            exit_code=0,
            error="",
            raw_result=result[0],
            vm=parse_vm_json(result[0]),
        )
    except subprocess.CalledProcessError as e:
        return GetVmResult(
            success=False,
            message=f"Failed to get VM {vm_id} information: {e}",
            exit_code=1,
            error=str(e),
            raw_result={},
            vm=None,
        )
    except json.JSONDecodeError as e:
        return GetVmResult(
            success=False,
            message=f"Failed to parse VM {vm_id} information: {e}",
            exit_code=1,
            error=str(e),
            raw_result={},
            vm=None,
        )
