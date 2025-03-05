import logging
from pd_ai_agent_core.core_types.session_service import SessionService
from pd_ai_agent_core.services.service_registry import ServiceRegistry
from pd_ai_agent_core.common.constants import VM_DATASOURCE_SERVICE_NAME
from pd_ai_agent_core.parallels_desktop.datasource import VirtualMachineDataSource

logger = logging.getLogger(__name__)


class VmDatasourceService(SessionService):
    def __init__(
        self,
        session_id: str,
        debug: bool = False,
        datasource: VirtualMachineDataSource = None,
    ):
        super().__init__(session_id)
        self.datasource = datasource
        self.debug = debug
        self.register()

    def name(self) -> str:
        return VM_DATASOURCE_SERVICE_NAME

    def register(self) -> None:
        """Register this service with the registry"""
        if not ServiceRegistry.register(
            self.session_id, VM_DATASOURCE_SERVICE_NAME, self
        ):
            logger.info(
                f"VmDatasourceService already registered for session {self.session_id}"
            )

    def unregister(self) -> None:
        """Unregister this service from the registry"""
        logger.info(f"VmDatasourceService unregistered for session {self.session_id}")

    def get_datasource(self) -> VirtualMachineDataSource:
        """Get the datasource for the session"""
        return self.datasource

    def set_datasource(self, datasource: VirtualMachineDataSource) -> None:
        """Set the datasource for the session"""
        self.datasource = datasource
