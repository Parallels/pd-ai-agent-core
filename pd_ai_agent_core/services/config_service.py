import os
import yaml
import json
from typing import Any, List
from pathlib import Path
from pd_ai_agent_core.core_types.session_service import SessionService
from pd_ai_agent_core.common.constants import CONFIG_SERVICE_NAME
from pd_ai_agent_core.services.service_registry import ServiceRegistry
from pd_ai_agent_core.common.defaults import USER_DATA_DIR
import logging

logger = logging.getLogger(__name__)


class ConfigService(SessionService):
    CONFIG_DIR = Path.home() / USER_DATA_DIR / "config"

    def __init__(
        self, session_id: str, config_file: str = "config.yaml", debug: bool = False
    ):
        self.config_file = self.CONFIG_DIR / f"{session_id}.{config_file}"
        self.config: dict = {}
        self._session_id = session_id
        self.debug = debug
        self._ensure_config_dir()
        self.load()
        self.register()

    def name(self) -> str:
        return CONFIG_SERVICE_NAME

    def register(self) -> None:
        """Register this service with the registry"""
        if not ServiceRegistry.register(self._session_id, CONFIG_SERVICE_NAME, self):
            logger.info(
                f"Config service already registered for session {self._session_id}"
            )
            return

    def unregister(self) -> None:
        """Unregister this service from the registry"""
        logger.info(f"Config service unregistered for session {self._session_id}")

    def _ensure_config_dir(self) -> None:
        """Ensure .parallels directory exists"""
        self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    def _parse_nested_key(self, key: str) -> List[str]:
        """Convert nested key to parts (e.g., 'database.host' -> ['database', 'host'])"""
        return key.split(".")

    def _set_nested_value(
        self, data: dict | list, parts: List[str], value: Any
    ) -> None:
        """Set value in nested dictionary"""
        for i, part in enumerate(parts[:-1]):
            if part.isdigit():  # Handle list indices
                idx = int(part)
                if not isinstance(data, list):
                    data = []  # type: ignore
                while len(data) <= idx:
                    data.append({})
            else:
                if not isinstance(data, dict) or part not in data:
                    data[part] = {}  # type: ignore
            data = data[part]  # type: ignore
        data[parts[-1]] = value  # type: ignore

    def _get_nested_value(
        self, data: dict, parts: List[str], default: Any = None
    ) -> Any:
        """Get value from nested dictionary"""
        for part in parts:
            if part.isdigit() and isinstance(data, list):
                idx = int(part)
                if idx >= len(data):
                    return default
                data = data[idx]
            elif isinstance(data, dict):
                if part not in data:
                    return default
                data = data[part]
            else:
                return default
        return data

    def load(self) -> None:
        """Load configuration from file and environment"""
        if self.config_file.exists():
            with open(self.config_file) as f:
                if str(self.config_file).endswith(".yaml"):
                    self.config = yaml.safe_load(f) or {}
                else:
                    self.config = json.load(f)
        else:
            self.config = {}
            self.save()

        # Override with environment variables
        for key, value in os.environ.items():
            if key.startswith("APP_"):
                # Convert APP_DATABASE__HOST to database.host
                config_key = key[4:].lower().replace("__", ".")
                # Parse value type
                if value.lower() in (
                    "true",
                    "false",
                    "t",
                    "f",
                    "1",
                    "0",
                    "yes",
                    "no",
                    "y",
                    "n",
                    "on",
                    "off",
                    "enabled",
                    "disabled",
                    "enable",
                    "disable",
                ):
                    value = value.lower() == "true"
                elif value.replace(".", "").isdigit():
                    value = float(value) if "." in value else int(value)
                elif value.startswith("[") and value.endswith("]"):
                    value = json.loads(value)

                parts = self._parse_nested_key(config_key)
                self._set_nested_value(self.config, parts, value)

    def save(self) -> None:
        """Save current configuration to file"""
        with open(self.config_file, "w") as f:
            if str(self.config_file).endswith(".yaml"):
                yaml.safe_dump(self.config, f)
            else:
                json.dump(self.config, f, indent=2)

    def get_key(self, key: str, default: Any = None) -> Any:
        """Get value for key with optional default"""
        env_key = f"APP_{key.upper().replace('.', '__')}"
        if env_key in os.environ:
            value = os.environ[env_key]
            # Parse value type
            if value.lower() in ("true", "false"):
                return value.lower() == "true"
            elif value.replace(".", "").isdigit():
                return float(value) if "." in value else int(value)
            return value

        parts = self._parse_nested_key(key)
        return self._get_nested_value(self.config, parts, default)

    def get_str_key(self, key: str, default: str = "") -> str:
        """Get string value for key"""
        return str(self.get_key(key, default))

    def get_int_key(self, key: str, default: int = 0) -> int:
        """Get integer value for key"""
        value = self.get_key(key, default)
        try:
            return int(float(value))  # Handle float strings
        except (TypeError, ValueError):
            return default

    def get_bool_key(self, key: str, default: bool = False) -> bool:
        """Get boolean value for key"""
        value = self.get_key(key, default)
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in (
                "true",
                "1",
                "yes",
                "on",
                "enable",
                "enabled",
                "t",
                "y",
            )
        return bool(value)

    def get_float_key(self, key: str, default: float = 0.0) -> float:
        """Get float value for key"""
        value = self.get_key(key, default)
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    def get_list_key(self, key: str, default: List[Any] | None = None) -> List[Any]:
        """Get list value for key"""
        default_list = default if default is not None else []
        value = self.get_key(key, default_list)
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return default_list
        return value if isinstance(value, list) else default_list

    def set_key(self, key: str, value: Any) -> None:
        """Set value for key and save configuration"""
        parts = self._parse_nested_key(key)
        self._set_nested_value(self.config, parts, value)
        self.save()
