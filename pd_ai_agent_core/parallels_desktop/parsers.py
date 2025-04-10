from pd_ai_agent_core.parallels_desktop.models.os import Os
from pd_ai_agent_core.parallels_desktop.models.update_package import AppPackage


def parse_linux_info(info_text) -> Os:
    """
    Parse Ubuntu system information text into a dictionary.

    Args:
        info_text (str): The raw text output from lsb_release or similar command

    Returns:
        dict: A dictionary containing the parsed Ubuntu information
    """
    result = {}

    # Split the text into lines and process each line
    for line in info_text.strip().split("\n"):
        # Skip empty lines
        if not line.strip():
            continue

        # Skip the "No LSB modules are available" line
        if "No LSB modules are available" in line:
            continue

        # Split by colon and handle the key-value pairs
        parts = line.split(":", 1)
        if len(parts) == 2:
            key = parts[0].strip()
            value = parts[1].strip()
            result[key] = value
    return Os(
        name=result["Distributor ID"],
        version=result["Release"],
        codename=result["Codename"],
        release=result["Description"],
    )


def parse_windows_info(info_text) -> Os:
    """
    Parse Windows system information text into an Os object.

    Args:
        info_text (str): The raw text output from Windows system information

    Returns:
        Os: An Os object containing the parsed Windows information
    """
    result = {}

    # Split the text into lines and process each line
    for line in info_text.strip().split("\n"):
        # Skip empty lines
        if not line.strip():
            continue

        # Split by colon and handle the key-value pairs
        parts = line.split(":", 1)
        if len(parts) == 2:
            key = parts[0].strip().replace("\x1b[32;1m", "").replace("\x1b[0m", "")
            value = parts[1].strip().replace("\x1b[32;1m", "").replace("\x1b[0m", "")
            result[key] = value

    # Extract relevant information for the Os object
    return Os(
        name=result.get("WindowsProductName", "Windows"),
        version=result.get("WindowsEditionId", ""),
        codename=result.get("WindowsProductId", ""),
        release=result.get("WindowsBuildLabEx", ""),
    )


def parse_macos_info(info_text) -> Os:
    """
    Parse macOS system information text into an Os object.

    Args:
        info_text (str): The raw text output from macOS system information

    Returns:
        Os: An Os object containing the parsed macOS information
    """
    result = {}

    # Split the text into lines and process each line
    for line in info_text.strip().split("\n"):
        # Skip empty lines
        if not line.strip():
            continue

        # Split by colon and handle the key-value pairs
        parts = line.split(":", 1)
        if len(parts) == 2:
            key = parts[0].strip()
            value = parts[1].strip()
            result[key] = value

    # Extract relevant information for the Os object
    return Os(
        name=result.get("ProductName", "macOS"),
        version=result.get("ProductVersion", ""),
        codename=result.get("BuildVersion", ""),
        release=result.get("ProductName", "macOS"),
    )


def parse_windows_updates(info_text) -> list[AppPackage]:
    """
    Parse Windows update information text into a list of dictionaries.

    Args:
        info_text (str): The raw text output from Windows update information

    Returns:
        list: A list of dictionaries containing the parsed Windows update information
    """
    updates = []

    # Split the text into lines
    lines = info_text.strip().split("\n")

    # Skip the header lines (first two lines)
    if len(lines) > 2:
        for line in lines[2:]:
            # Skip empty lines
            if not line.strip():
                continue

            # Split the line by whitespace, but keep the title together
            parts = line.split()

            # Ensure we have at least 5 parts (ComputerName, Status, KB, Size, Title)
            if len(parts) >= 5:
                # Extract the KB number
                kb = parts[2]

                # Extract the size
                size = parts[3]

                # The title is everything after the size
                title = " ".join(parts[4:])

                # Create a dictionary for this update
                update = AppPackage(
                    name=kb,
                    version=size,
                    release=title,
                    codename="",
                    description="",
                )

                updates.append(update)

    return updates


def parse_macos_updates(info_text) -> list[AppPackage]:
    """
    Parse macOS update information text into a list of UpdatePackage objects.

    Args:
        info_text (str): The raw text output from macOS update information

    Returns:
        list[UpdatePackage]: A list of UpdatePackage objects containing the parsed macOS update information
    """
    updates = []

    # Split the text into lines
    lines = info_text.strip().split("\n")

    # Find the line that indicates the start of the update list
    start_index = 0
    for i, line in enumerate(lines):
        if "Software Update found the following new or updated software:" in line:
            start_index = i + 1
            break

    # Process each update entry
    current_update = {}
    for line in lines[start_index:]:
        # Skip empty lines
        if not line.strip():
            continue

        # Check if this is a new update entry (starts with *)
        if line.strip().startswith("*"):
            # If we have a previous update, add it to the list
            if current_update:
                updates.append(
                    AppPackage(
                        name=current_update.get("label", ""),
                        version=current_update.get("version", ""),
                        release=current_update.get("title", ""),
                        codename=current_update.get("label", ""),
                        description=current_update.get("size", ""),
                    )
                )

            # Start a new update entry
            current_update = {}

            # Extract the label
            label_parts = line.strip().split(":", 1)
            if len(label_parts) == 2:
                current_update["label"] = label_parts[1].strip()
        else:
            # This is a continuation of the current update
            # Extract key-value pairs
            parts = line.strip().split(",")
            for part in parts:
                if ":" in part:
                    key, value = part.split(":", 1)
                    key = key.strip()
                    value = value.strip()

                    if key == "Title":
                        current_update["title"] = value
                    elif key == "Version":
                        current_update["version"] = value
                    elif key == "Size":
                        current_update["size"] = value

    # Add the last update if there is one
    if current_update:
        updates.append(
            AppPackage(
                name=current_update.get("label", ""),
                version=current_update.get("version", ""),
                release=current_update.get("title", ""),
                codename=current_update.get("label", ""),
                description=current_update.get("size", ""),
            )
        )

    return updates


def parse_debian_updates(info_text) -> list[AppPackage]:
    """
    Parse Debian Linux update information text into a list of UpdatePackage objects.

    Args:
        info_text (str): The raw text output from Debian update information

    Returns:
        list[UpdatePackage]: A list of UpdatePackage objects containing the parsed Debian update information
    """
    updates = []

    # Split the text into lines
    lines = info_text.strip().split("\n")

    # Process each line
    for line in lines:
        # Skip empty lines
        if not line.strip():
            continue

        # Split the line by "/" to separate package name and version info
        parts = line.split("/", 1)
        if len(parts) == 2:
            package_name = parts[0].strip()
            version_info = parts[1].strip()

            # Split the version info by spaces
            version_parts = version_info.split()
            if len(version_parts) >= 2:
                version = version_parts[0]
                codename = version_parts[1]

                # The architecture is the last part
                architecture = version_parts[-1] if len(version_parts) > 2 else ""

                # Create an UpdatePackage object for this update
                update = AppPackage(
                    name=package_name.replace("~", ""),
                    version=codename.replace("~", ""),
                    release=package_name.replace("~", ""),
                    codename=version.replace("~", ""),
                    description=architecture.replace("~", ""),
                )

                updates.append(update)

    return updates


def parse_windows_installed_apps(info_text) -> list[AppPackage]:
    """
    Parse Windows installed applications information text into a list of AppPackage objects.

    Args:
        info_text (str): The raw text output from Windows installed applications information

    Returns:
        list[AppPackage]: A list of AppPackage objects containing the parsed Windows installed applications information
    """
    apps = []

    # Split the text into lines
    lines = info_text.strip().split("\n")

    # Skip the header line (first line)
    if len(lines) > 1:
        for line in lines[1:]:
            # Skip empty lines
            if not line.strip():
                continue

            # Process each line, splitting by multiple spaces
            parts = []
            current_part = []
            spaces = 0

            for char in line:
                if char == " ":
                    spaces += 1
                    if (
                        spaces >= 2
                    ):  # If we hit multiple spaces, consider it a delimiter
                        if current_part:  # If we have collected some characters
                            parts.append("".join(current_part).strip())
                            current_part = []
                    else:
                        current_part.append(char)
                else:
                    spaces = 0
                    current_part.append(char)

            # Add the last part if there is one
            if current_part:
                parts.append("".join(current_part).strip())

            # Ensure we have at least 4 parts (Caption, InstallState, Name, Vendor, Version)
            if len(parts) >= 5:
                caption = parts[0]
                install_state = parts[1]
                name = parts[2]
                vendor = parts[3]
                version = parts[4]

                # Create an AppPackage object for this app
                app = AppPackage(
                    name=name,
                    version=version,
                    release=caption,
                    codename=install_state,
                    description=vendor,
                )

                apps.append(app)

    return apps


def parse_macos_installed_apps(info_text) -> list[AppPackage]:
    """
    Parse macOS installed applications information from JSON into a list of AppPackage objects.

    Args:
        info_text (str): The JSON output from macOS system_profiler SPApplicationsDataType -json

    Returns:
        list[AppPackage]: A list of AppPackage objects containing the parsed macOS installed applications information
    """
    apps = []

    try:
        import json

        # Parse the JSON string into a Python dictionary
        data = json.loads(info_text)

        # Extract the applications list
        applications = data.get("SPApplicationsDataType", [])

        for app in applications:
            name = app.get("_name", "")
            version = app.get("version", "")
            arch_kind = app.get("arch_kind", "")
            obtained_from = app.get("obtained_from", "")

            # Create an AppPackage object for this app
            app_package = AppPackage(
                name=name,
                version=version,
                release=arch_kind,
                codename=obtained_from,
                description="-",
            )

            apps.append(app_package)

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
    except Exception as e:
        print(f"Error processing applications data: {e}")

    return apps


def parse_debian_installed_apps(info_text) -> list[AppPackage]:
    """
    Parse Debian Linux installed applications information text into a list of AppPackage objects.

    Args:
        info_text (str): The raw text output from Debian installed applications information

    Returns:
        list[AppPackage]: A list of AppPackage objects containing the parsed Debian installed applications information
    """
    apps = []

    # Split the text into lines
    lines = info_text.strip().split("\n")

    # Process each line
    for line in lines:
        # Skip empty lines
        if not line.strip():
            continue

        # Split the line by tab or multiple spaces
        parts = line.split("\t")
        if len(parts) == 1:
            # If no tabs, try splitting by multiple spaces
            parts = []
            current_part = []
            spaces = 0

            for char in line:
                if char == " ":
                    spaces += 1
                    if (
                        spaces >= 2
                    ):  # If we hit multiple spaces, consider it a delimiter
                        if current_part:  # If we have collected some characters
                            parts.append("".join(current_part).strip())
                            current_part = []
                    else:
                        current_part.append(char)
                else:
                    spaces = 0
                    current_part.append(char)

            # Add the last part if there is one
            if current_part:
                parts.append("".join(current_part).strip())

        # Ensure we have at least 2 parts (package name and version)
        if len(parts) >= 2:
            package_name = parts[0].strip()
            version = parts[1].strip()

            # Create an AppPackage object for this app
            app = AppPackage(
                name=package_name.replace("~", ""),
                version=version.replace("~", ""),
                release=package_name.replace("~", ""),
                codename="debian",
                description="",
            )

            apps.append(app)

    return apps
