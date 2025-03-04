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
from pd_ai_agent_core.parallels_desktop.helpers import get_prlsrvctl_command
from pd_ai_agent_core.parallels_desktop.models.operation_result import OperationResult
import logging

logger = logging.getLogger(__name__)


async def send_problem_report(
    session_id: str, vm_id: str, message: Message
) -> OperationResult:
    try:
        notifications = ServiceRegistry.get(
            session_id, NOTIFICATION_SERVICE_NAME, NotificationService
        )
        cmd: List[str] = [str(get_prlsrvctl_command()), "problem-report", "--send"]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            shell=False,
        )
        if result.returncode == 0:
            output = result.stdout.strip()
            report_id = None
            if "problem report was successfully sent with id:" in output.lower():
                report_id = output.split(":")[-1].strip()
            if report_id:
                success_message = create_success_notification_message(
                    session_id=session_id,
                    channel=vm_id,
                    message="Problem report sent successfully",
                    details=f"The problem report was sent successfully with id: {report_id}",
                )
                await notifications.send(success_message)
                return OperationResult(
                    success=True,
                    message="Problem report sent successfully",
                    exit_code=result.returncode,
                    error=result.stderr,
                )
        else:
            error_message = create_error_notification_message(
                session_id=session_id,
                channel=vm_id,
                message="Error sending problem report",
                details="The problem report was not sent successfully",
            )
            await notifications.send(error_message)
            return OperationResult(
                success=False,
                message="Error sending problem report",
                exit_code=result.returncode,
                error=result.stderr,
            )
    except Exception as e:
        logger.error(f"Error sending problem report: {e}")
        error_message = create_error_notification_message(
            session_id=session_id,
            channel=vm_id,
            message=f"Error sending problem report: {e}",
            details="The problem report was not sent successfully",
        )
        await notifications.send(error_message)
        return OperationResult(
            success=False,
            message=f"Error sending problem report: {e}",
            exit_code=1,
            error=str(e),
        )
