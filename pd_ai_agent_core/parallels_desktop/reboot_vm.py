from typing import List
import subprocess
from pd_ai_agent_core.common.constants import NOTIFICATION_SERVICE_NAME
from pd_ai_agent_core.services.service_registry import ServiceRegistry
from pd_ai_agent_core.services.notification_service import NotificationService
from pd_ai_agent_core.messages.message import Message
from pd_ai_agent_core.messages.notification_message import (
    create_success_notification_message,
    create_error_notification_message,
)
from pd_ai_agent_core.parallels_desktop.helpers import get_prlctl_command
from pd_ai_agent_core.parallels_desktop.datasource import VirtualMachineDataSource
import logging
from pd_ai_agent_core.parallels_desktop.models.operation_result import OperationResult

logger = logging.getLogger(__name__)


async def reboot_vm(session_id: str, vm_id: str, message: Message) -> OperationResult:
    try:
        notifications = ServiceRegistry.get(
            session_id, NOTIFICATION_SERVICE_NAME, NotificationService
        )
        vm_datasource = VirtualMachineDataSource.get_instance()
        vm = vm_datasource.get_vm(vm_id)
        if vm:
            cmd: List[str] = [str(get_prlctl_command()), "restart", vm_id]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                shell=False,
            )
            if result.returncode == 0:
                success_message = create_success_notification_message(
                    session_id=session_id,
                    channel=vm_id,
                    message=f"VM {vm.name} restarted successfully",
                    details=f"The VM {vm.name} was restarted successfully",
                )
                opResult = OperationResult(
                    success=True,
                    message=f"VM {vm.name} restarted successfully",
                    exit_code=result.returncode,
                    error=result.stderr,
                )
                await notifications.send(success_message)
                return opResult
            else:
                error_message = create_error_notification_message(
                    session_id=session_id,
                    channel=vm_id,
                    message=f"Error restarting VM {vm.name}",
                    details=f"The VM {vm.name} was not restarted successfully",
                )
                opResult = OperationResult(
                    success=False,
                    message=f"Error restarting VM {vm.name}",
                    exit_code=result.returncode,
                    error=result.stderr,
                )
                await notifications.send(error_message)
                return opResult
        else:
            error_message = create_error_notification_message(
                session_id=session_id,
                channel=vm_id,
                message="VM not found",
                details="The VM was not found",
            )
            opResult = OperationResult(
                success=False,
                message="VM not found",
                exit_code=result.returncode,
                error=result.stderr,
            )
            await notifications.send(error_message)
            return opResult
    except Exception as e:
        logger.error(f"Error restarting VM: {e}")
        error_message = create_error_notification_message(
            session_id=session_id,
            channel=vm_id,
            message=f"Error restarting VM: {e}",
            details="The VM was not restarted successfully",
        )
        await notifications.send(error_message)
        opResult = OperationResult(
            success=False,
            message=f"Error restarting VM: {e}",
            exit_code=1,
            error=str(e),
        )
        return opResult
