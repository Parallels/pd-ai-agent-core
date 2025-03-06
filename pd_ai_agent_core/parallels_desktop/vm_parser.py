from typing import Dict, Any
from pd_ai_agent_core.parallels_desktop.models.virtual_machine import (
    VirtualMachine,
    GuestTools,
    MouseAndKeyboard,
    USBAndBluetooth,
    StartupAndShutdown,
    Optimization,
    TravelMode,
    Security,
    Expiration,
    Modality,
    Fullscreen,
    Coherence,
    TimeSynchronization,
    SMBIOSSettings,
    Hardware,
    CPU,
    Memory,
    Video,
    MemoryQuota,
    Hdd0,
    Cdrom0,
    Net0,
    Sound0,
    HostSharedFolders,
    SharedApplications,
    Network,
    MiscellaneousSharing,
    Advanced,
    SmartGuard,
    Usb,
    SharedProfile,
    SmartMount,
)


def parse_vm_json(data: Dict[str, Any]) -> VirtualMachine:
    """Parse VM JSON data into a VM object"""

    # Parse nested objects first
    guest_tools = GuestTools(data=data)

    mouse_keyboard = MouseAndKeyboard(data=data)

    usb_bluetooth = USBAndBluetooth(data=data)

    startup_shutdown = StartupAndShutdown(data=data)

    optimization = Optimization(data=data)

    travel_mode = TravelMode(data=data)

    security = Security(data=data)

    smart_guard = SmartGuard(data=data)

    modality = Modality(data=data)

    fullscreen = Fullscreen(data=data)

    coherence = Coherence(data=data)

    time_sync = TimeSynchronization(data=data)

    expiration = Expiration(data=data)

    smbios = SMBIOSSettings(data=data)

    # Parse Hardware components
    cpu = CPU(data=data)

    memory = Memory(data=data)

    video = Video(data=data)

    memory_quota = MemoryQuota(data=data)

    hdd0 = Hdd0(data=data)

    cdrom0 = Cdrom0(data=data)

    usb = Usb(data=data)

    net0 = Net0(data=data)

    sound0 = Sound0(data=data)

    hardware = Hardware(
        cpu=cpu,
        memory=memory,
        video=video,
        memory_quota=memory_quota,
        hdd0=hdd0,
        cdrom0=cdrom0,
        usb=usb,
        net0=net0,
        sound0=sound0,
    )

    host_shared_folders = HostSharedFolders(data=data)

    shared_profile = SharedProfile(data=data)

    shared_applications = SharedApplications(data=data)

    smart_mount = SmartMount(data=data)

    network = Network(data=data)

    misc_sharing = MiscellaneousSharing(data=data)

    advanced = Advanced(data=data)

    # Create and return the VM object
    return VirtualMachine(
        id=data["ID"] if "ID" in data else "",
        name=data["Name"] if "Name" in data else "",
        description=data["Description"] if "Description" in data else "",
        type=data["Type"] if "Type" in data else "",
        state=data["State"] if "State" in data else "",
        os=data["OS"] if "OS" in data else "",
        template=data["Template"] if "Template" in data else "",
        uptime=int(data["Uptime"]) if "Uptime" in data else 0,
        home_path=data["Home path"] if "Home path" in data else "",
        home=data["Home"] if "Home" in data else "",
        restore_image=data["Restore Image"] if "Restore Image" in data else "",
        screenshot="",  # Not in sample JSON
        guest_tools=guest_tools,
        mouse_and_keyboard=mouse_keyboard,
        usb_and_bluetooth=usb_bluetooth,
        startup_and_shutdown=startup_shutdown,
        optimization=optimization,
        travel_mode=travel_mode,
        security=security,
        smart_guard=smart_guard,
        modality=modality,
        fullscreen=fullscreen,
        coherence=coherence,
        time_synchronization=time_sync,
        expiration=expiration,
        boot_order=data["Boot order"] if "Boot order" in data else "",
        bios_type=data["BIOS type"] if "BIOS type" in data else "",
        efi_secure_boot=data["EFI Secure boot"] if "EFI Secure boot" in data else "",
        allow_select_boot_device=(
            data["Allow select boot device"]
            if "Allow select boot device" in data
            else ""
        ),
        external_boot_device=(
            data["External boot device"] if "External boot device" in data else ""
        ),
        smbios_settings=smbios,
        hardware=hardware,
        host_shared_folders=host_shared_folders,
        host_defined_sharing=(
            data["Host defined sharing"] if "Host defined sharing" in data else ""
        ),
        shared_profile=shared_profile,
        shared_applications=shared_applications,
        smart_mount=smart_mount,
        network=network,
        miscellaneous_sharing=misc_sharing,
        advanced=advanced,
        print_management=None,  # Not in sample JSON
        guest_shared_folders=None,  # Not in sample JSON
    )
