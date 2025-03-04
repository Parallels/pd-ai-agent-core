import threading
import subprocess
import time
import json
import logging
import selectors
from pd_ai_agent_core.services.service_registry import ServiceRegistry
from pd_ai_agent_core.services.notification_service import NotificationService
from pd_ai_agent_core.services.log_service import LogService
from pd_ai_agent_core.common.constants import (
    GLOBAL_EVENT_CHANNEL,
    NOTIFICATION_SERVICE_NAME,
    LOGGER_SERVICE_NAME,
    VM_EVENT_MONITOR_SERVICE_NAME,
    BACKGROUND_SERVICE_NAME,
)
from pd_ai_agent_core.events.prlctl_event_item import PrlctlEventItem
import os
import pty
from pd_ai_agent_core.messages.event_message import create_event_message
from pd_ai_agent_core.parallels_desktop.datasource import VirtualMachineDataSource
from pd_ai_agent_core.parallels_desktop.get_vms import get_vms, get_vm
from pd_ai_agent_core.parallels_desktop.vm_parser import parse_vm_json
from pd_ai_agent_core.core_types.session_service import SessionService
from pd_ai_agent_core.services.background_service import BackgroundAgentService
from pd_ai_agent_core.parallels_desktop.helpers import get_prlctl_command
from pd_ai_agent_core.messages.constants import (
    VM_STATE_STARTED,
    VM_STATE_STOPPED,
    VM_STATE_SUSPENDED,
    VM_STATE_PAUSED,
    VM_STATE_CHANGED,
    VM_SYNC_SCREENSHOT,
)

logger = logging.getLogger(__name__)


class VmEventMonitorService(SessionService):
    def __init__(
        self,
        session_id: str,
        debug: bool = False,
        datasource: VirtualMachineDataSource = None,
    ):
        self._process = None
        self._running = False
        self._thread = None
        self._lock = threading.Lock()
        self.debug = debug
        self._session_id = session_id

        notifications_service = ServiceRegistry.get(
            session_id, NOTIFICATION_SERVICE_NAME, NotificationService
        )
        logger_service = ServiceRegistry.get(
            session_id, LOGGER_SERVICE_NAME, LogService
        )
        background_service = ServiceRegistry.get(
            session_id, BACKGROUND_SERVICE_NAME, BackgroundAgentService
        )
        if notifications_service is None:
            raise ValueError(f"Notification service not found for session {session_id}")
        if logger_service is None:
            raise ValueError(f"Logger service not found for session {session_id}")
        if background_service is None:
            raise ValueError(f"Background service not found for session {session_id}")
        self.notification_service = notifications_service
        self.logger_service = logger_service
        self.background_service = background_service
        self.datasource = datasource
        if self.datasource is None:
            raise ValueError(f"Datasource not found for session {session_id}")
        self.register()

    def name(self) -> str:
        return VM_EVENT_MONITOR_SERVICE_NAME

    def register(self) -> None:
        """Register this service with the registry"""
        if not ServiceRegistry.register(
            self._session_id, VM_EVENT_MONITOR_SERVICE_NAME, self
        ):
            logger.info(
                f"VM event monitor service already registered for session {self._session_id}"
            )
            return

        logger.info(
            f"VM event monitor service registered for session {self._session_id}"
        )

    def unregister(self) -> None:
        """Unregister this service from the registry"""
        self.stop()
        logger.info(
            f"VM event monitor service unregistered for session {self._session_id}"
        )

    def set_debug(self, debug: bool):
        self.debug = debug

    def start(self):
        """Start the VM event monitor service"""
        with self._lock:
            # Check if already running
            if self._running:
                logger.info("VM event monitor service is already running.")
                return

            # Double check process and thread status
            if self._process and self._process.poll() is None:
                logger.info("VM event monitor process is still running.")
                return

            if self._thread and self._thread.is_alive():
                logger.info("VM event monitor thread is still alive.")
                return

            logger.info("Starting VM event monitor service")
            self._running = True
            self._thread = threading.Thread(target=self._monitor_events, daemon=True)
            self._thread.start()

    def stop(self):
        """Stop the VM event monitor service"""
        with self._lock:
            self._running = False

            if self._process:
                logger.info("Terminating VM event monitor process")
                self._process.terminate()
                try:
                    self._process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    logger.warning("Force killing VM event monitor process")
                    self._process.kill()

            if self._thread:
                logger.info("Waiting for VM event monitor thread to finish")
                self._thread.join()

    def _monitor_events(self):
        """Monitor VM events in a background thread"""
        selector = selectors.DefaultSelector()

        while self._running:
            try:
                master_fd, slave_fd = pty.openpty()

                self._process = subprocess.Popen(
                    [get_prlctl_command(), "monitor-events", "--json"],
                    stdout=slave_fd,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,
                    close_fds=True,
                )

                os.close(slave_fd)
                logger.info("Started monitoring VM events")

                selector.register(master_fd, selectors.EVENT_READ)

                buffer = ""
                while self._running and self._process.poll() is None:
                    events = selector.select(timeout=1)
                    for key, _ in events:
                        if key.fileobj == master_fd:
                            try:
                                data = os.read(master_fd, 1024).decode(
                                    "utf-8", errors="replace"
                                )
                                if not data:
                                    break

                                buffer += data
                                while "\n" in buffer:
                                    line, buffer = buffer.split("\n", 1)
                                    line = line.strip()
                                    if line:
                                        if self.debug:
                                            logger.debug(f"STDOUT: {line}")
                                        self._handle_event(line)

                            except OSError as e:
                                logger.error(f"Error reading from PTY: {e}")
                                break

                selector.unregister(master_fd)
            except Exception as e:
                logger.exception(f"Error in VM event monitor: {e}")
                time.sleep(5)

            finally:
                if self._process and self._process.poll() is None:
                    self._process.terminate()
                    try:
                        self._process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        self._process.kill()

                if self._running:
                    logger.warning(
                        "VM event monitor process exited unexpectedly. Restarting in 5 seconds..."
                    )
                    time.sleep(5)

    def _handle_event(self, line: str):
        """Handle a single event line from the VM monitor"""
        try:
            event_data = json.loads(line)
            event_item = PrlctlEventItem.from_dict(event_data)
            event_name = "vm_changed"
            event_type = "unknown"
            event_data = {}
            if event_item.vm_id:
                event_data["vm_id"] = event_item.vm_id
            if event_item.additional_info:
                for key, value in event_item.additional_info.items():
                    if (
                        key == "Vm state name"
                        and value != "cloning"
                        and value != "unknown"
                    ):
                        event_name = "state_changed"
                        event_type = value
                        self.datasource.update_vm_state(event_item.vm_id, value)
                        # notification_message = create_info_notification_message(
                        #     session_id=self._session_id,
                        #     channel=event_item.vm_id,
                        #     message=f"VM {event_item.vm_id} state changed to {value}",
                        # )
                        # self.notification_service.send_sync(notification_message)
                        # notification_message = create_info_notification_message(
                        #     session_id=self._session_id,
                        #     channel=GLOBAL_NOTIFICATION_CHANNEL,
                        #     message=f"VM {event_item.vm_id} state changed to {value}",
                        # )
                        # self.notification_service.send_sync(notification_message)
                    if event_type == "running":
                        self.background_service.post_message(
                            VM_SYNC_SCREENSHOT,
                            {"vm_id": event_item.vm_id},
                        )
                        self.background_service.post_message(
                            VM_STATE_STARTED,
                            {"vm_id": event_item.vm_id},
                        )
                        self.background_service.post_message(
                            VM_STATE_CHANGED,
                            {"vm_id": event_item.vm_id},
                        )
                    if event_type == "suspended":
                        self.background_service.post_message(
                            VM_STATE_SUSPENDED,
                            {"vm_id": event_item.vm_id},
                        )
                        self.background_service.post_message(
                            VM_STATE_CHANGED,
                            {"vm_id": event_item.vm_id},
                        )
                    if event_type == "stopped":
                        self.background_service.post_message(
                            VM_STATE_STOPPED,
                            {"vm_id": event_item.vm_id},
                        )
                        self.background_service.post_message(
                            VM_STATE_CHANGED,
                            {"vm_id": event_item.vm_id},
                        )
                    if event_type == "paused":
                        self.background_service.post_message(
                            VM_STATE_PAUSED,
                            {"vm_id": event_item.vm_id},
                        )
                        self.background_service.post_message(
                            VM_STATE_CHANGED,
                            {"vm_id": event_item.vm_id},
                        )
            if event_item.event_name == "vm_config_changed":
                event_name = "config_changed"
                event_type = "unknown"
            if event_item.event_name == "vm_snapshot_created":
                event_name = "snapshot_created"
                event_type = "unknown"
            if event_item.event_name == "vm_added":
                event_name = "vm_added"
                event_type = "vm_added"
                vms = get_vms()
                if vms.success:
                    for vm in vms.vm:
                        vm_model = parse_vm_json(vm)
                        self.datasource.update_vm(vm_model)
                new_vm = get_vm(event_item.vm_id)
                if new_vm.success:
                    event_data["vm"] = json.dumps(new_vm.vm)
            if event_item.event_name == "vm_unregistered":
                event_name = "vm_unregistered"
                event_type = "vm_unregistered"
                self.datasource.remove_vm(event_item.vm_id)
            event_message = create_event_message(
                session_id=self._session_id,
                channel=GLOBAL_EVENT_CHANNEL,
                event_name=event_name,
                event_type=event_type,
                event_data=event_data,
            )

            # only broadcast if event_type is known
            if event_type != "unknown":
                self.notification_service.broadcast_sync(event_message)

        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e} | Line: {line}")
        except Exception as e:
            logger.exception(f"Error handling VM event: {e}")
