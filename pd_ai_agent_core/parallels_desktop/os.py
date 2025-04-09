from pd_ai_agent_core.services.service_registry import ServiceRegistry
from pd_ai_agent_core.services.notification_service import NotificationService
from pd_ai_agent_core.services.vm_datasource_service import VmDatasourceService
from pd_ai_agent_core.common import (
    NOTIFICATION_SERVICE_NAME,
    VM_DATASOURCE_SERVICE_NAME,
)
from pd_ai_agent_core.messages import (
    create_clean_agent_function_call_chat_message,
)
from pd_ai_agent_core.core_types.llm_chat_ai_agent import (
    LlmChatAgentResponse,
)
from pd_ai_agent_core.parallels_desktop.models.virtual_machine import VirtualMachine
from typing import List
from pd_ai_agent_core.parallels_desktop.execute_on_vm import execute_on_vm
from pd_ai_agent_core.parallels_desktop.parsers import (
    parse_linux_info,
    parse_macos_info,
    parse_windows_info,
    parse_debian_updates,
    parse_macos_updates,
    parse_windows_updates,
    parse_windows_installed_apps,
    parse_macos_installed_apps,
    parse_debian_installed_apps,
)
from pd_ai_agent_core.parallels_desktop.models.os import Os
from pd_ai_agent_core.parallels_desktop.models.update_package import (
    UpdatePackageResponse,
)


def update_packages_list_cmd(os: str) -> List[str]:
    if os.lower() == "ubuntu":
        return ["sudo", "apt", "update"]
    elif os.lower() == "debian":
        return ["sudo", "apt", "update"]
    elif os.lower() == "macos":
        return []
    elif os.lower() == "windows":
        return []
    else:
        return []


def list_all_packages_cmd(os: str) -> List[str]:
    if os.lower() == "ubuntu":
        return ["sudo", "apt-mark", "showmanual", "|", "xargs", "dpkg-query", "-W"]
    elif os.lower() == "debian":
        return ["sudo", "apt-mark", "showmanual", "|", "xargs", "dpkg-query", "-W"]
    elif os.lower() == "macos":
        return ["system_profiler", "SPApplicationsDataType", "-json"]
    elif os.lower() == "windows":
        return [
            "wmic",
            "product",
            "get",
            "Name,Version,Vendor,Caption,InstallState",
        ]
    else:
        return []


def get_inventory(vm_id: str, os: str) -> UpdatePackageResponse:
    os = get_std_os(os)
    response = UpdatePackageResponse(
        updates=[],
        installed_apps=[],
        os=os,
        vm_id=vm_id,
        warnings=[],
        errors=[],
    )
    cmd = list_all_packages_cmd(os)
    result = execute_on_vm(vm_id, command=" ".join(cmd))
    if result.exit_code != 0:
        response.errors.append(f"Failed to get updates: {result.error}")
    return_result = None
    if os.lower() == "ubuntu":
        return_result = parse_debian_installed_apps(result.output)
    elif os.lower() == "debian":
        return_result = parse_debian_installed_apps(result.output)
    elif os.lower() == "macos":
        return_result = parse_macos_installed_apps(result.output)
    elif os.lower() == "windows":
        return_result = parse_windows_installed_apps(result.output)
    response.installed_apps = return_result or []
    return response


def list_updates_cmd(os: str) -> List[str]:
    if os.lower() == "ubuntu":
        return ["sudo", "apt", "list", "--upgradable"]
    elif os.lower() == "debian":
        return ["sudo", "apt", "list", "--upgradable"]
    elif os.lower() == "macos":
        return ["softwareupdate", "-l"]
    elif os.lower() == "windows":
        return [
            "pwsh",
            "-Command",
            '"Install-Module PSWindowsUpdate -Force -AllowClobber; Import-Module PSWindowsUpdate; Get-WindowsUpdate"',
        ]
    else:
        return []


def get_updates(vm_id: str, os: str, upgradable: bool = False) -> UpdatePackageResponse:
    os = get_std_os(os)
    response = UpdatePackageResponse(
        updates=[],
        installed_apps=[],
        os=os,
        vm_id=vm_id,
        warnings=[],
        errors=[],
    )
    cmd = None
    if os.lower() == "ubuntu" or os.lower() == "debian":
        # first lets update the package list
        update_packages = execute_on_vm(
            vm_id, command=" ".join(update_packages_list_cmd(os))
        )
        if update_packages.exit_code != 0:
            response.errors.append(
                f"Failed to update packages: {update_packages.error}"
            )
    cmd = list_updates_cmd(os)
    result = execute_on_vm(vm_id, command=" ".join(cmd))
    if result.exit_code != 0:
        response.errors.append(f"Failed to get updates: {result.error}")
    return_result = None
    if os.lower() == "ubuntu":
        return_result = parse_debian_updates(result.output)
    elif os.lower() == "debian":
        return_result = parse_debian_updates(result.output)
    elif os.lower() == "macos":
        return_result = parse_macos_updates(result.output)
    elif os.lower() == "windows":
        return_result = parse_windows_updates(result.output)
    response.updates = return_result or []
    return response


def update_packages_cmd(os: str) -> List[str]:
    if os.lower() == "ubuntu":
        return ["sudo", "apt", "upgrade", "-y"]
    elif os.lower() == "debian":
        return ["sudo", "apt", "upgrade", "-y"]
    elif os.lower() == "macos":
        # return ["softwareupdate", "-i", "-a", "-R"]
        return []
    elif os.lower() == "windows":
        return [
            "pwsh",
            "-Command",
            '"Install-Module PSWindowsUpdate -Force -AllowClobber; Import-Module PSWindowsUpdate; Install-WindowsUpdate -AcceptAll -AutoReboot"',
        ]
    else:
        return []


def update_vm_packages(vm_id: str, os: str) -> tuple[bool, str]:
    os = get_std_os(os)
    cmd = None
    if os.lower() == "ubuntu" or os.lower() == "debian":
        # first lets update the package list
        execute_on_vm(vm_id, command=" ".join(update_packages_list_cmd(os)))

    cmd = update_packages_cmd(os)
    result = execute_on_vm(vm_id, command=" ".join(cmd))
    if result.exit_code != 0:
        return False, result.error
    return True, result.output


def get_os_version_cmd(os: str) -> List[str]:
    if os.lower() == "ubuntu":
        return ["lsb_release", "-a"]
    elif os.lower() == "debian":
        return ["lsb_release", "-a"]
    elif os.lower() == "macos":
        return ["sw_vers"]
    elif os.lower() == "windows":
        return ["pwsh", "-Command", "Get-ComputerInfo"]
    else:
        return []


def get_os_version(vm_id: str, os: str) -> Os:
    os = get_std_os(os)
    cmd = get_os_version_cmd(os)
    result = execute_on_vm(vm_id, command=" ".join(cmd))
    if result.exit_code != 0:
        raise RuntimeError(f"Failed to get OS version: {result.error}")
    return_result = None
    # lets parse the output
    if os.lower() == "windows":
        return_result = parse_windows_info(result.output)
    elif os.lower() == "macos":
        return_result = parse_macos_info(result.output)
    else:
        return_result = parse_linux_info(result.output)
    print(f"OS Version: {return_result}")
    return return_result


def get_std_os(os: str) -> str:
    if os == "win-11":
        return "windows"
    if os == "win-10":
        return "windows"
    if os == "macos":
        return "macos"
    if os == "macosx":
        return "macos"
    if os == "ubuntu":
        return "ubuntu"
    if os == "debian":
        return "debian"
    return os


def get_vm_details(
    session_context: dict, context_variables: dict, vm_id: str
) -> tuple[VirtualMachine | None, LlmChatAgentResponse | None]:
    ns = ServiceRegistry.get(
        session_context["session_id"],
        NOTIFICATION_SERVICE_NAME,
        NotificationService,
    )
    data = ServiceRegistry.get(
        session_context["session_id"],
        VM_DATASOURCE_SERVICE_NAME,
        VmDatasourceService,
    )
    if not data:
        ns.send_sync(
            create_clean_agent_function_call_chat_message(
                session_context["session_id"],
                session_context["channel"],
                session_context["linked_message_id"],
                session_context["is_partial"],
            )
        )
        return None, LlmChatAgentResponse(
            status="error",
            message="No vm datasource provided",
        )
    vm_details = data.datasource.get_vm(vm_id)
    if not vm_details:
        ns.send_sync(
            create_clean_agent_function_call_chat_message(
                session_context["session_id"],
                session_context["channel"],
                session_context["linked_message_id"],
                session_context["is_partial"],
            )
        )
        return None, LlmChatAgentResponse(
            status="error",
            message="No vm details provided",
        )
    return vm_details, None
