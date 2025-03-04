import subprocess
from typing import List
import os
import base64
from pd_ai_agent_core.parallels_desktop.helpers import get_prlctl_command
from pd_ai_agent_core.parallels_desktop.models.get_vm_screenshot_result import (
    GetVmScreenshotResult,
)
from pd_ai_agent_core.helpers.image import get_dominant_border_color


def get_vm_screenshot(vm_id: str) -> GetVmScreenshotResult:
    """Get a screenshot of the VM"""
    if not vm_id:
        raise ValueError("VM ID is required")
    try:
        temp_filename = f"{vm_id}_{os.urandom(4).hex()}.png"
        cmd: List[str] = [
            get_prlctl_command(),
            "capture",
            vm_id,
            "--file",
            temp_filename,
        ]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
            shell=False,
        )
        if result.returncode != 0:
            return GetVmScreenshotResult(
                success=False,
                message=result.stderr,
                raw_screenshot=None,
                screenshot=None,
                border_color=None,
            )
        # Generate random temp filename to avoid collisions
        with open(temp_filename, "rb") as f:
            screenshot_data = f.read()
        os.remove(temp_filename)
        screenshot_data_str = _serialize_image(screenshot_data)
        border_color = get_dominant_border_color(screenshot_data_str)
        return GetVmScreenshotResult(
            success=True,
            message=f"Screenshot saved to {vm_id}.png",
            raw_screenshot=screenshot_data,
            screenshot=screenshot_data_str,
            border_color=border_color,
        )
    except Exception as e:
        return GetVmScreenshotResult(
            success=False,
            message=f"Failed to get screenshot for VM {vm_id}: {e}",
            raw_screenshot=None,
            screenshot=None,
            border_color=None,
        )


def _serialize_image(image_bytes: bytes) -> str:
    # Convert bytes to a base64 string
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    # JSON object with the base64 image
    return base64_image
