import os
from pd_ai_agent_core.parallels_desktop.constants import (
    PRLCTL_COMMAND,
    PRLSRVCTL_COMMAND,
)


def get_prlctl_command():
    basePath = os.getenv("PRLCTL_PATH", "/usr/local/bin")
    return os.path.join(basePath, PRLCTL_COMMAND)


def get_prlsrvctl_command():
    basePath = os.getenv("PRLCTL_PATH", "/usr/local/bin")
    return os.path.join(basePath, PRLSRVCTL_COMMAND)
