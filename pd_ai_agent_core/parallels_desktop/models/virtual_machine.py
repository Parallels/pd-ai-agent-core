from typing import Dict, Any, Optional, List
import json


class Advanced:
    vm_hostname_synchronization: str
    public_ssh_keys_synchronization: str
    show_developer_tools: str
    swipe_from_edges: str
    share_host_location: str
    rosetta_linux: str

    def __init__(self, data: Dict[str, Any]) -> None:
        if "Advanced" in data:
            advanced = data["Advanced"]
            if "VM hostname synchronization" in advanced:
                self.vm_hostname_synchronization = advanced[
                    "VM hostname synchronization"
                ]
            if "Public SSH keys synchronization" in advanced:
                self.public_ssh_keys_synchronization = advanced[
                    "Public SSH keys synchronization"
                ]
            if "Show developer tools" in advanced:
                self.show_developer_tools = advanced["Show developer tools"]
            if "Swipe from edges" in advanced:
                self.swipe_from_edges = advanced["Swipe from edges"]
            if "Share host location" in advanced:
                self.share_host_location = advanced["Share host location"]
            if "Rosetta Linux" in advanced:
                self.rosetta_linux = advanced["Rosetta Linux"]

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        for attr in [
            "vm_hostname_synchronization",
            "public_ssh_keys_synchronization",
            "show_developer_tools",
            "swipe_from_edges",
            "share_host_location",
            "rosetta_linux",
        ]:
            if hasattr(self, attr):
                result[attr] = getattr(self, attr)
        return result


class Coherence:
    show_windows_systray_in_mac_menu: str
    auto_switch_to_full_screen: str

    def __init__(self, data: Dict[str, Any]) -> None:
        if "Coherence" in data:
            coherence = data["Coherence"]
            if "Show Windows systray in Mac menu" in coherence:
                self.show_windows_systray_in_mac_menu = coherence[
                    "Show Windows systray in Mac menu"
                ]
            if "Auto-switch to full screen" in coherence:
                self.auto_switch_to_full_screen = coherence[
                    "Auto-switch to full screen"
                ]

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        for attr in ["show_windows_systray_in_mac_menu", "auto_switch_to_full_screen"]:
            if hasattr(self, attr):
                result[attr] = getattr(self, attr)
        return result


class SmartGuard:
    enabled: bool

    def __init__(self, data: Dict[str, Any]) -> None:
        if "Smart Guard" in data:
            smart_guard = data["Smart Guard"]
            if "enabled" in smart_guard:
                self.enabled = smart_guard["enabled"]

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        if hasattr(self, "enabled"):
            result["enabled"] = self.enabled
        return result


class Expiration:
    enabled: bool

    def __init__(self, data: Dict[str, Any]) -> None:
        if "Expiration" in data:
            expiration = data["Expiration"]
            if "enabled" in expiration:
                self.enabled = expiration["enabled"]

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        if hasattr(self, "enabled"):
            result["enabled"] = self.enabled
        return result


class Fullscreen:
    use_all_displays: str
    activate_spaces_on_click: str
    optimize_for_games: str
    gamma_control: str
    scale_view_mode: str

    def __init__(self, data: Dict[str, Any]) -> None:
        if "Fullscreen" in data:
            fullscreen = data["Fullscreen"]
            if "Use all displays" in fullscreen:
                self.use_all_displays = fullscreen["Use all displays"]
            if "Activate spaces on click" in fullscreen:
                self.activate_spaces_on_click = fullscreen["Activate spaces on click"]
            if "Optimize for games" in fullscreen:
                self.optimize_for_games = fullscreen["Optimize for games"]
            if "Gamma control" in fullscreen:
                self.gamma_control = fullscreen["Gamma control"]
            if "Scale view mode" in fullscreen:
                self.scale_view_mode = fullscreen["Scale view mode"]

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        for attr in [
            "use_all_displays",
            "activate_spaces_on_click",
            "optimize_for_games",
            "gamma_control",
            "scale_view_mode",
        ]:
            if hasattr(self, attr):
                result[attr] = getattr(self, attr)
        return result


class GuestTools:
    state: str
    version: str

    def __init__(self, data: Dict[str, Any]) -> None:
        if "GuestTools" in data:
            guest_tools = data["GuestTools"]
            if "state" in guest_tools:
                self.state = guest_tools["state"]
            if "version" in guest_tools:
                self.version = guest_tools["version"]

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        if hasattr(self, "state"):
            result["state"] = self.state
        if hasattr(self, "version"):
            result["version"] = self.version
        return result


class Cdrom0:
    enabled: bool
    port: str
    image: str
    state: Optional[str]

    def __init__(self, data: Dict[str, Any]) -> None:
        if "Hardware" in data:
            hardware = data["Hardware"]
            if "cdrom0" in hardware:
                cdrom0 = hardware["cdrom0"]
                if "enabled" in cdrom0:
                    self.enabled = cdrom0["enabled"]
                if "port" in cdrom0:
                    self.port = cdrom0["port"]
                if "image" in cdrom0:
                    self.image = cdrom0["image"]
                if "state" in cdrom0:
                    self.state = cdrom0["state"]

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        for attr in ["enabled", "port", "image", "state"]:
            if hasattr(self, attr):
                result[attr] = getattr(self, attr)
        return result


class Usb:
    enabled: bool

    def __init__(self, data: Dict[str, Any]) -> None:
        if "Hardware" in data:
            hardware = data["Hardware"]
            if "usb" in hardware:
                usb = hardware["usb"]
                if "enabled" in usb:
                    self.enabled = usb["enabled"]

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        if hasattr(self, "enabled"):
            result["enabled"] = self.enabled
        return result


class CPU:
    cpus: int
    auto: str
    vt_x: bool
    hotplug: bool
    accl: str
    mode: int
    type: str

    def __init__(self, data: Dict[str, Any]) -> None:
        if "Hardware" in data:
            hardware = data["Hardware"]
            if "cpu" in hardware:
                cpu = hardware["cpu"]
                if "cpus" in cpu:
                    self.cpus = cpu["cpus"]
                if "auto" in cpu:
                    self.auto = cpu["auto"]
                if "VT-x" in cpu:
                    self.vt_x = cpu["VT-x"]
                if "hotplug" in cpu:
                    self.hotplug = cpu["hotplug"]
                if "accl" in cpu:
                    self.accl = cpu["accl"]
                if "mode" in cpu:
                    self.mode = cpu["mode"]
                if "type" in cpu:
                    self.type = cpu["type"]

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        for attr in ["cpus", "auto", "vt_x", "hotplug", "accl", "mode", "type"]:
            if hasattr(self, attr):
                result[attr] = getattr(self, attr)
        return result


class Hdd0:
    enabled: bool
    port: str
    image: str
    type: str
    size: str
    online_compact: str

    def __init__(self, data: Dict[str, Any]) -> None:
        if "Hardware" in data:
            hardware = data["Hardware"]
            if "hdd0" in hardware:
                hdd0 = hardware["hdd0"]
                if "enabled" in hdd0:
                    self.enabled = hdd0["enabled"]
                if "port" in hdd0:
                    self.port = hdd0["port"]
                if "image" in hdd0:
                    self.image = hdd0["image"]
                if "type" in hdd0:
                    self.type = hdd0["type"]
                if "size" in hdd0:
                    self.size = hdd0["size"]
                if "online_compact" in hdd0:
                    self.online_compact = hdd0["online_compact"]

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        for attr in ["enabled", "port", "image", "type", "size", "online_compact"]:
            if hasattr(self, attr):
                result[attr] = getattr(self, attr)
        return result


class Memory:
    size: str
    auto: str
    hotplug: bool

    def __init__(self, data: Dict[str, Any]) -> None:
        if "Hardware" in data:
            hardware = data["Hardware"]
            if "memory" in hardware:
                memory = hardware["memory"]
                if "size" in memory:
                    self.size = memory["size"]
                if "auto" in memory:
                    self.auto = memory["auto"]
                if "hotplug" in memory:
                    self.hotplug = memory["hotplug"]

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        for attr in ["size", "auto", "hotplug"]:
            if hasattr(self, attr):
                result[attr] = getattr(self, attr)
        return result


class MemoryQuota:
    auto: str

    def __init__(self, data: Dict[str, Any]) -> None:
        if "Hardware" in data:
            hardware = data["Hardware"]
            if "memory_quota" in hardware:
                memory_quota = hardware["memory_quota"]
                if "auto" in memory_quota:
                    self.auto = memory_quota["auto"]

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        if hasattr(self, "auto"):
            result["auto"] = self.auto
        return result


class Net0:
    enabled: bool
    type: str
    mac: str
    card: str
    dhcp: Optional[str]
    iface: Optional[str]

    def __init__(self, data: Dict[str, Any]) -> None:
        if "Hardware" in data:
            hardware = data["Hardware"]
            if "net0" in hardware:
                net0 = hardware["net0"]
                if "enabled" in net0:
                    self.enabled = net0["enabled"]
                if "type" in net0:
                    self.type = net0["type"]
                if "mac" in net0:
                    self.mac = net0["mac"]
                if "card" in net0:
                    self.card = net0["card"]
                if "dhcp" in net0:
                    self.dhcp = net0["dhcp"]
                if "iface" in net0:
                    self.iface = net0["iface"]

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        for attr in ["enabled", "type", "mac", "card", "dhcp", "iface"]:
            if hasattr(self, attr):
                result[attr] = getattr(self, attr)
        return result


class Sound0:
    enabled: bool
    output: str
    mixer: str

    def __init__(self, data: Dict[str, Any]) -> None:
        if "Hardware" in data:
            hardware = data["Hardware"]
            if "sound0" in hardware:
                sound0 = hardware["sound0"]
                if "enabled" in sound0:
                    self.enabled = sound0["enabled"]
                if "output" in sound0:
                    self.output = sound0["output"]
                if "mixer" in sound0:
                    self.mixer = sound0["mixer"]

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        for attr in ["enabled", "output", "mixer"]:
            if hasattr(self, attr):
                result[attr] = getattr(self, attr)
        return result


class Video:
    adapter_type: str
    size: str
    the_3_d_acceleration: str
    vertical_sync: str
    high_resolution: str
    high_resolution_in_guest: str
    native_scaling_in_guest: str
    automatic_video_memory: str

    def __init__(self, data: Dict[str, Any]) -> None:
        if "Hardware" in data:
            hardware = data["Hardware"]
            if "video" in hardware:
                video = hardware["video"]
                if "adapter-type" in video:
                    self.adapter_type = video["adapter-type"]
                if "size" in video:
                    self.size = video["size"]
                if "3d-acceleration" in video:
                    self.the_3_d_acceleration = video["3d-acceleration"]
                if "vertical-sync" in video:
                    self.vertical_sync = video["vertical-sync"]
                if "high-resolution" in video:
                    self.high_resolution = video["high-resolution"]
                if "high-resolution-in-guest" in video:
                    self.high_resolution_in_guest = video["high-resolution-in-guest"]
                if "native-scaling-in-guest" in video:
                    self.native_scaling_in_guest = video["native-scaling-in-guest"]
                if "automatic-video-memory" in video:
                    self.automatic_video_memory = video["automatic-video-memory"]

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        for attr in [
            "adapter_type",
            "size",
            "the_3_d_acceleration",
            "vertical_sync",
            "high_resolution",
            "high_resolution_in_guest",
            "native_scaling_in_guest",
            "automatic_video_memory",
        ]:
            if hasattr(self, attr):
                result[attr] = getattr(self, attr)
        return result


class Hardware:
    cpu: CPU
    memory: Memory
    video: Video
    memory_quota: MemoryQuota
    hdd0: Hdd0
    cdrom0: Cdrom0
    usb: Usb
    net0: Net0
    sound0: Sound0

    def __init__(
        self,
        cpu: CPU,
        memory: Memory,
        video: Video,
        memory_quota: MemoryQuota,
        hdd0: Hdd0,
        cdrom0: Cdrom0,
        usb: Usb,
        net0: Net0,
        sound0: Sound0,
    ) -> None:
        self.cpu = cpu
        self.memory = memory
        self.video = video
        self.memory_quota = memory_quota
        self.hdd0 = hdd0
        self.cdrom0 = cdrom0
        self.usb = usb
        self.net0 = net0
        self.sound0 = sound0

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        for attr in [
            "cpu",
            "memory",
            "video",
            "memory_quota",
            "hdd0",
            "cdrom0",
            "usb",
            "net0",
            "sound0",
        ]:
            if hasattr(self, attr) and getattr(self, attr) is not None:
                result[attr] = getattr(self, attr).to_dict()
        return result


class HostSharedFolders:
    enabled: bool

    def __init__(self, data: Dict[str, Any]) -> None:
        if "Host Shared Folders" in data:
            host_shared_folders = data["Host Shared Folders"]
            if "enabled" in host_shared_folders:
                self.enabled = host_shared_folders["enabled"]

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        if hasattr(self, "enabled"):
            result["enabled"] = self.enabled
        return result


class MiscellaneousSharing:
    shared_clipboard_mode: str
    shared_cloud: str

    def __init__(self, data: Dict[str, Any]) -> None:
        if "Miscellaneous Sharing" in data:
            miscellaneous_sharing = data["Miscellaneous Sharing"]
            if "Shared clipboard mode" in miscellaneous_sharing:
                self.shared_clipboard_mode = miscellaneous_sharing[
                    "Shared clipboard mode"
                ]
            if "Shared cloud" in miscellaneous_sharing:
                self.shared_cloud = miscellaneous_sharing["Shared cloud"]

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        for attr in ["shared_clipboard_mode", "shared_cloud"]:
            if hasattr(self, attr):
                result[attr] = getattr(self, attr)
        return result


class Modality:
    opacity_percentage: int
    stay_on_top: str
    show_on_all_spaces: str
    capture_mouse_clicks: str

    def __init__(self, data: Dict[str, Any]) -> None:
        if "Modality" in data:
            modality = data["Modality"]
            if "Opacity (percentage)" in modality:
                self.opacity_percentage = modality["Opacity (percentage)"]
            if "Stay on top" in modality:
                self.stay_on_top = modality["Stay on top"]
            if "Show on all spaces" in modality:
                self.show_on_all_spaces = modality["Show on all spaces"]
            if "Capture mouse clicks" in modality:
                self.capture_mouse_clicks = modality["Capture mouse clicks"]

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        for attr in [
            "opacity_percentage",
            "stay_on_top",
            "show_on_all_spaces",
            "capture_mouse_clicks",
        ]:
            if hasattr(self, attr):
                result[attr] = getattr(self, attr)
        return result


class MouseAndKeyboard:
    smart_mouse_optimized_for_games: str
    sticky_mouse: str
    smooth_scrolling: str
    keyboard_optimization_mode: str

    def __init__(self, data: Dict[str, Any]) -> None:
        if "Mouse and Keyboard" in data:
            mouse_and_keyboard = data["Mouse and Keyboard"]
            if "Smart mouse optimized for games" in mouse_and_keyboard:
                self.smart_mouse_optimized_for_games = mouse_and_keyboard[
                    "Smart mouse optimized for games"
                ]
            if "Sticky mouse" in mouse_and_keyboard:
                self.sticky_mouse = mouse_and_keyboard["Sticky mouse"]
            if "Smooth scrolling" in mouse_and_keyboard:
                self.smooth_scrolling = mouse_and_keyboard["Smooth scrolling"]
            if "Keyboard optimization mode" in mouse_and_keyboard:
                self.keyboard_optimization_mode = mouse_and_keyboard[
                    "Keyboard optimization mode"
                ]

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        for attr in [
            "smart_mouse_optimized_for_games",
            "sticky_mouse",
            "smooth_scrolling",
            "keyboard_optimization_mode",
        ]:
            if hasattr(self, attr):
                result[attr] = getattr(self, attr)
        return result


class IPAddress:
    type: str
    ip: str

    def __init__(self, type: str, ip: str) -> None:
        self.type = type
        self.ip = ip

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        for attr in ["type", "ip"]:
            if hasattr(self, attr):
                result[attr] = getattr(self, attr)
        return result


class IPAddresses:
    ip_addresses: List[IPAddress] = []

    def __init__(self, data: Dict[str, Any]) -> None:
        if "Network" in data:
            network = data["Network"]
            if "ipAddresses" in network:
                ip_addresses = network["ipAddresses"]

                for ip_address in ip_addresses:
                    type = ""
                    ip = ""
                    if "type" in ip_address:
                        type = ip_address["type"]
                    if "ip" in ip_address:
                        ip = ip_address["ip"]
                    self.ip_addresses.append(IPAddress(type=type, ip=ip))
            else:
                self.ip_addresses = []

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        if hasattr(self, "ip_addresses"):
            result["ip_addresses"] = [
                ip.to_dict() for ip in self.ip_addresses if ip is not None
            ]
        return result


class NetworkConditioner:
    bandwidth: str
    packet_loss: str
    delay: str

    def __init__(self, data: Dict[str, Any]) -> None:
        if "Bandwidth" in data:
            self.bandwidth = data["Bandwidth"]
        if "Packet Loss" in data:
            self.packet_loss = data["Packet Loss"]
        if "Delay" in data:
            self.delay = data["Delay"]

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        if hasattr(self, "bandwidth"):
            result["bandwidth"] = self.bandwidth
        if hasattr(self, "packet_loss"):
            result["packet_loss"] = self.packet_loss
        if hasattr(self, "delay"):
            result["delay"] = self.delay
        return result


class Network:
    conditioned: str
    ip_addresses: List[IPAddress] = []
    inbound: NetworkConditioner
    outbound: NetworkConditioner

    def __init__(self, data: Dict[str, Any]) -> None:
        if "Network" in data:
            network = data["Network"]
            if "Conditioned" in network:
                self.conditioned = network["Conditioned"]
            if "ipAddresses" in network:
                ipAddresses = (
                    network["ipAddresses"]
                    if isinstance(network["ipAddresses"], list)
                    else []
                )
                for ipaddress in ipAddresses:
                    if "type" in ipaddress:
                        type = ipaddress["type"]
                    if "ip" in ipaddress:
                        ip = ipaddress["ip"]
                    self.ip_addresses.append(IPAddress(type=type, ip=ip))

            if "Inbound" in network:
                inbound = NetworkConditioner(network["Inbound"])
                self.inbound = inbound
            if "Outbound" in network:
                outbound = NetworkConditioner(network["Outbound"])
                self.outbound = outbound

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        if hasattr(self, "ip_addresses"):
            result["ip_addresses"] = [
                ip.to_dict() for ip in self.ip_addresses if ip is not None
            ]
        if hasattr(self, "conditioned"):
            result["conditioned"] = self.conditioned
        if hasattr(self, "inbound"):
            result["inbound"] = self.inbound.to_dict()
        if hasattr(self, "outbound"):
            result["outbound"] = self.outbound.to_dict()
        return result


class Optimization:
    faster_virtual_machine: str
    hypervisor_type: str
    adaptive_hypervisor: str
    disabled_windows_logo: str
    auto_compress_virtual_disks: str
    nested_virtualization: str
    pmu_virtualization: str
    longer_battery_life: str
    show_battery_status: str
    resource_quota: str

    def __init__(self, data: Dict[str, Any]) -> None:
        if "Optimization" in data:
            optimization = data["Optimization"]
            if "Faster virtual machine" in optimization:
                self.faster_virtual_machine = optimization["Faster virtual machine"]
            if "Hypervisor type" in optimization:
                self.hypervisor_type = optimization["Hypervisor type"]
            if "Adaptive hypervisor" in optimization:
                self.adaptive_hypervisor = optimization["Adaptive hypervisor"]
            if "Disabled Windows logo" in optimization:
                self.disabled_windows_logo = optimization["Disabled Windows logo"]
            if "Auto compress virtual disks" in optimization:
                self.auto_compress_virtual_disks = optimization[
                    "Auto compress virtual disks"
                ]
            if "Nested virtualization" in optimization:
                self.nested_virtualization = optimization["Nested virtualization"]
            if "PMU virtualization" in optimization:
                self.pmu_virtualization = optimization["PMU virtualization"]
            if "Longer battery life" in optimization:
                self.longer_battery_life = optimization["Longer battery life"]
            if "Show battery status" in optimization:
                self.show_battery_status = optimization["Show battery status"]
            if "Resource quota" in optimization:
                self.resource_quota = optimization["Resource quota"]

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        for attr in [
            "faster_virtual_machine",
            "hypervisor_type",
            "adaptive_hypervisor",
            "disabled_windows_logo",
            "auto_compress_virtual_disks",
            "nested_virtualization",
            "pmu_virtualization",
            "longer_battery_life",
            "show_battery_status",
            "resource_quota",
        ]:
            if hasattr(self, attr):
                result[attr] = getattr(self, attr)
        return result


class PrintManagement:
    synchronize_with_host_printers: str
    synchronize_default_printer: str
    show_host_printer_ui: str

    def __init__(
        self,
        synchronize_with_host_printers: str,
        synchronize_default_printer: str,
        show_host_printer_ui: str,
    ) -> None:
        self.synchronize_with_host_printers = synchronize_with_host_printers
        self.synchronize_default_printer = synchronize_default_printer
        self.show_host_printer_ui = show_host_printer_ui

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        for attr in [
            "synchronize_with_host_printers",
            "synchronize_default_printer",
            "show_host_printer_ui",
        ]:
            if hasattr(self, attr):
                result[attr] = getattr(self, attr)
        return result


class Security:
    encrypted: str
    tpm_enabled: str
    tpm_type: str
    custom_password_protection: str
    configuration_is_locked: str
    protected: str
    archived: str
    packed: str

    def __init__(self, data: Dict[str, Any]) -> None:
        if "Security" in data:
            security = data["Security"]
            if "Encrypted" in security:
                self.encrypted = security["Encrypted"]
            if "TPM enabled" in security:
                self.tpm_enabled = security["TPM enabled"]
            if "TPM type" in security:
                self.tpm_type = security["TPM type"]
            if "Custom password protection" in security:
                self.custom_password_protection = security["Custom password protection"]
            if "Configuration is locked" in security:
                self.configuration_is_locked = security["Configuration is locked"]
            if "Protected" in security:
                self.protected = security["Protected"]
            if "Archived" in security:
                self.archived = security["Archived"]
            if "Packed" in security:
                self.packed = security["Packed"]

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        for attr in [
            "encrypted",
            "tpm_enabled",
            "tpm_type",
            "custom_password_protection",
            "configuration_is_locked",
            "protected",
            "archived",
            "packed",
        ]:
            if hasattr(self, attr):
                result[attr] = getattr(self, attr)
        return result


class SharedProfile:
    enabled: bool

    def __init__(self, data: Dict[str, Any]) -> None:
        if "Shared Profile" in data:
            shared_profile = data["Shared Profile"]
            if "enabled" in shared_profile:
                self.enabled = shared_profile["enabled"]

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        if hasattr(self, "enabled"):
            result["enabled"] = self.enabled
        return result


class SharedApplications:
    enabled: bool
    host_to_guest_apps_sharing: str
    guest_to_host_apps_sharing: str
    show_guest_apps_folder_in_dock: str
    show_guest_notifications: str
    bounce_dock_icon_when_app_flashes: str

    def __init__(self, data: Dict[str, Any]) -> None:
        if "Shared Applications" in data:
            shared_applications = data["Shared Applications"]
            if "enabled" in shared_applications:
                self.enabled = shared_applications["enabled"]
            if "Host-to-guest apps sharing" in shared_applications:
                self.host_to_guest_apps_sharing = shared_applications[
                    "Host-to-guest apps sharing"
                ]
            if "Guest-to-host apps sharing" in shared_applications:
                self.guest_to_host_apps_sharing = shared_applications[
                    "Guest-to-host apps sharing"
                ]
            if "Show guest apps folder in Dock" in shared_applications:
                self.show_guest_apps_folder_in_dock = shared_applications[
                    "Show guest apps folder in Dock"
                ]
            if "Show guest notifications" in shared_applications:
                self.show_guest_notifications = shared_applications[
                    "Show guest notifications"
                ]
            if "Bounce dock icon when app flashes" in shared_applications:
                self.bounce_dock_icon_when_app_flashes = shared_applications[
                    "Bounce dock icon when app flashes"
                ]

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        for attr in [
            "enabled",
            "host_to_guest_apps_sharing",
            "guest_to_host_apps_sharing",
            "show_guest_apps_folder_in_dock",
            "show_guest_notifications",
            "bounce_dock_icon_when_app_flashes",
        ]:
            if hasattr(self, attr):
                result[attr] = getattr(self, attr)
        return result


class SmartMount:
    enabled: bool

    def __init__(self, data: Dict[str, Any]) -> None:
        if "SmartMount" in data:
            smart_mount = data["SmartMount"]
            if "enabled" in smart_mount:
                self.enabled = smart_mount["enabled"]

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        if hasattr(self, "enabled"):
            result["enabled"] = self.enabled
        return result


class SMBIOSSettings:
    bios_version: str
    system_serial_number: str
    board_manufacturer: str

    def __init__(self, data: Dict[str, Any]) -> None:
        if "SMBIOS settings" in data:
            smbios_settings = data["SMBIOS settings"]
            if "BIOS version" in smbios_settings:
                self.bios_version = smbios_settings["BIOS version"]
            if "System serial number" in smbios_settings:
                self.system_serial_number = smbios_settings["System serial number"]
            if "Board manufacturer" in smbios_settings:
                self.board_manufacturer = smbios_settings["Board manufacturer"]

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        for attr in ["bios_version", "system_serial_number", "board_manufacturer"]:
            if hasattr(self, attr):
                result[attr] = getattr(self, attr)
        return result


class StartupAndShutdown:
    autostart: str
    autostart_delay: int
    autostop: str
    startup_view: str
    on_shutdown: str
    on_window_close: str
    pause_idle: str
    undo_disks: str

    def __init__(self, data: Dict[str, Any]) -> None:
        if "Startup and Shutdown" in data:
            startup_and_shutdown = data["Startup and Shutdown"]
            if "Autostart" in startup_and_shutdown:
                self.autostart = startup_and_shutdown["Autostart"]
            if "Autostart delay" in startup_and_shutdown:
                self.autostart_delay = startup_and_shutdown["Autostart delay"]
            if "Autostop" in startup_and_shutdown:
                self.autostop = startup_and_shutdown["Autostop"]
            if "Startup view" in startup_and_shutdown:
                self.startup_view = startup_and_shutdown["Startup view"]
            if "On shutdown" in startup_and_shutdown:
                self.on_shutdown = startup_and_shutdown["On shutdown"]
            if "On window close" in startup_and_shutdown:
                self.on_window_close = startup_and_shutdown["On window close"]
            if "Pause idle" in startup_and_shutdown:
                self.pause_idle = startup_and_shutdown["Pause idle"]
            if "Undo disks" in startup_and_shutdown:
                self.undo_disks = startup_and_shutdown["Undo disks"]

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        for attr in [
            "autostart",
            "autostart_delay",
            "autostop",
            "startup_view",
            "on_shutdown",
            "on_window_close",
            "pause_idle",
            "undo_disks",
        ]:
            if hasattr(self, attr):
                result[attr] = getattr(self, attr)
        return result


class TimeSynchronization:
    enabled: bool
    smart_mode: str
    interval_in_seconds: int
    timezone_synchronization_disabled: str

    def __init__(self, data: Dict[str, Any]) -> None:
        if "Time Synchronization" in data:
            time_synchronization = data["Time Synchronization"]
            if "enabled" in time_synchronization:
                self.enabled = time_synchronization["enabled"]
            if "Smart mode" in time_synchronization:
                self.smart_mode = time_synchronization["Smart mode"]
            if "Interval (in seconds)" in time_synchronization:
                self.interval_in_seconds = time_synchronization["Interval (in seconds)"]
            if "Timezone synchronization disabled" in time_synchronization:
                self.timezone_synchronization_disabled = time_synchronization[
                    "Timezone synchronization disabled"
                ]

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        for attr in [
            "enabled",
            "smart_mode",
            "interval_in_seconds",
            "timezone_synchronization_disabled",
        ]:
            if hasattr(self, attr):
                result[attr] = getattr(self, attr)
        return result


class TravelMode:
    enter_condition: str
    enter_threshold: int
    quit_condition: str

    def __init__(self, data: Dict[str, Any]) -> None:
        if "Travel mode" in data:
            travel_mode = data["Travel mode"]
            if "Enter condition" in travel_mode:
                self.enter_condition = travel_mode["Enter condition"]
            if "Enter threshold" in travel_mode:
                self.enter_threshold = travel_mode["Enter threshold"]
            if "Quit condition" in travel_mode:
                self.quit_condition = travel_mode["Quit condition"]

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        for attr in ["enter_condition", "enter_threshold", "quit_condition"]:
            if hasattr(self, attr):
                result[attr] = getattr(self, attr)
        return result


class USBAndBluetooth:
    automatic_sharing_cameras: str
    automatic_sharing_bluetooth: str
    automatic_sharing_smart_cards: str
    automatic_sharing_gamepads: str
    support_usb_30: str

    def __init__(self, data: Dict[str, Any]) -> None:
        if "USB and Bluetooth" in data:
            usb_and_bluetooth = data["USB and Bluetooth"]
            if "automatic_sharing_cameras" in usb_and_bluetooth:
                self.automatic_sharing_cameras = usb_and_bluetooth[
                    "automatic_sharing_cameras"
                ]
            if "automatic_sharing_bluetooth" in usb_and_bluetooth:
                self.automatic_sharing_bluetooth = usb_and_bluetooth[
                    "automatic_sharing_bluetooth"
                ]
            if "automatic_sharing_smart_cards" in usb_and_bluetooth:
                self.automatic_sharing_smart_cards = usb_and_bluetooth[
                    "automatic_sharing_smart_cards"
                ]
            if "automatic_sharing_gamepads" in usb_and_bluetooth:
                self.automatic_sharing_gamepads = usb_and_bluetooth[
                    "automatic_sharing_gamepads"
                ]
            if "support_usb_30" in usb_and_bluetooth:
                self.support_usb_30 = usb_and_bluetooth["support_usb_30"]

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        for attr in [
            "automatic_sharing_cameras",
            "automatic_sharing_bluetooth",
            "automatic_sharing_smart_cards",
            "automatic_sharing_gamepads",
            "support_usb_30",
        ]:
            if hasattr(self, attr):
                result[attr] = getattr(self, attr)
        return result


class VirtualMachine:
    id: str
    name: str
    description: str
    type: str
    state: str
    os: str
    template: str
    uptime: int
    home_path: str
    home: str
    restore_image: str
    screenshot: str
    guest_tools: GuestTools
    mouse_and_keyboard: MouseAndKeyboard
    usb_and_bluetooth: USBAndBluetooth
    startup_and_shutdown: StartupAndShutdown
    optimization: Optimization
    travel_mode: TravelMode
    security: Security
    smart_guard: SmartGuard
    modality: Modality
    fullscreen: Fullscreen
    coherence: Coherence
    time_synchronization: TimeSynchronization
    expiration: Expiration
    boot_order: str
    bios_type: str
    efi_secure_boot: str
    allow_select_boot_device: str
    external_boot_device: str
    smbios_settings: SMBIOSSettings
    hardware: Hardware
    host_shared_folders: HostSharedFolders
    host_defined_sharing: str
    shared_profile: SharedProfile
    shared_applications: SharedApplications
    smart_mount: SmartMount
    network: Network
    miscellaneous_sharing: MiscellaneousSharing
    advanced: Advanced
    print_management: Optional[PrintManagement]
    guest_shared_folders: Optional[Expiration]

    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        type: str,
        state: str,
        os: str,
        template: str,
        uptime: int,
        home_path: str,
        home: str,
        restore_image: str,
        screenshot: str,
        guest_tools: GuestTools,
        mouse_and_keyboard: MouseAndKeyboard,
        usb_and_bluetooth: USBAndBluetooth,
        startup_and_shutdown: StartupAndShutdown,
        optimization: Optimization,
        travel_mode: TravelMode,
        security: Security,
        smart_guard: SmartGuard,
        modality: Modality,
        fullscreen: Fullscreen,
        coherence: Coherence,
        time_synchronization: TimeSynchronization,
        expiration: Expiration,
        boot_order: str,
        bios_type: str,
        efi_secure_boot: str,
        allow_select_boot_device: str,
        external_boot_device: str,
        smbios_settings: SMBIOSSettings,
        hardware: Hardware,
        host_shared_folders: HostSharedFolders,
        host_defined_sharing: str,
        shared_profile: SharedProfile,
        shared_applications: SharedApplications,
        smart_mount: SmartMount,
        network: Network,
        miscellaneous_sharing: MiscellaneousSharing,
        advanced: Advanced,
        print_management: Optional[PrintManagement],
        guest_shared_folders: Optional[Expiration],
    ) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.type = type
        self.state = state
        self.os = os
        self.template = template
        self.uptime = uptime
        self.home_path = home_path
        self.home = home
        self.restore_image = restore_image
        self.screenshot = screenshot
        self.guest_tools = guest_tools
        self.mouse_and_keyboard = mouse_and_keyboard
        self.usb_and_bluetooth = usb_and_bluetooth
        self.startup_and_shutdown = startup_and_shutdown
        self.optimization = optimization
        self.travel_mode = travel_mode
        self.security = security
        self.smart_guard = smart_guard
        self.modality = modality
        self.fullscreen = fullscreen
        self.coherence = coherence
        self.time_synchronization = time_synchronization
        self.expiration = expiration
        self.boot_order = boot_order
        self.bios_type = bios_type
        self.efi_secure_boot = efi_secure_boot
        self.allow_select_boot_device = allow_select_boot_device
        self.external_boot_device = external_boot_device
        self.smbios_settings = smbios_settings
        self.hardware = hardware
        self.host_shared_folders = host_shared_folders
        self.host_defined_sharing = host_defined_sharing
        self.shared_profile = shared_profile
        self.shared_applications = shared_applications
        self.smart_mount = smart_mount
        self.network = network
        self.miscellaneous_sharing = miscellaneous_sharing
        self.advanced = advanced
        self.print_management = print_management
        self.guest_shared_folders = guest_shared_folders

    def to_dict(self) -> Dict[str, Any]:
        result = {}

        # Add basic attributes
        for attr in [
            "id",
            "name",
            "description",
            "type",
            "state",
            "os",
            "template",
            "uptime",
            "home_path",
            "home",
            "restore_image",
            "screenshot",
            "boot_order",
            "bios_type",
            "efi_secure_boot",
            "allow_select_boot_device",
            "external_boot_device",
            "host_defined_sharing",
        ]:
            if hasattr(self, attr):
                result[attr] = getattr(self, attr)

        # Add nested objects with defensive checks
        for attr in [
            "guest_tools",
            "mouse_and_keyboard",
            "usb_and_bluetooth",
            "startup_and_shutdown",
            "optimization",
            "travel_mode",
            "security",
            "smart_guard",
            "modality",
            "fullscreen",
            "coherence",
            "time_synchronization",
            "expiration",
            "smbios_settings",
            "hardware",
            "host_shared_folders",
            "shared_profile",
            "shared_applications",
            "smart_mount",
            "network",
            "miscellaneous_sharing",
            "advanced",
        ]:
            if hasattr(self, attr) and getattr(self, attr) is not None:
                result[attr] = getattr(self, attr).to_dict()

        # Add optional fields if they exist
        if hasattr(self, "print_management") and self.print_management:
            result["print_management"] = self.print_management.to_dict()
        if hasattr(self, "guest_shared_folders") and self.guest_shared_folders:
            result["guest_shared_folders"] = self.guest_shared_folders.to_dict()

        return result

    def to_json(self, indent: Optional[int] = None) -> str:
        """
        Convert the VirtualMachine object to a JSON string.

        Args:
            indent: Number of spaces for indentation in the JSON output. If None, the output will be compact.

        Returns:
            A JSON string representation of the VirtualMachine.
        """
        return json.dumps(self.to_dict(), indent=indent)
