import pydantic
import json


class AppPackage(pydantic.BaseModel):
    name: str
    version: str
    release: str
    codename: str
    description: str

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "version": self.version,
            "release": self.release,
            "codename": self.codename,
            "description": self.description,
        }

    def to_string(self) -> str:
        return f"{self.name} {self.version} {self.release} {self.codename} {self.description}"

    def to_list(self) -> list[str]:
        return [self.name, self.version, self.release, self.codename, self.description]

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


def updates_to_string(updates: list[AppPackage]) -> str:
    if len(updates) == 0:
        return "No updates found"
    return "\n".join([update.to_string() for update in updates])


def app_packages_to_csv(app_packages: list[AppPackage]) -> str:
    if len(app_packages) == 0:
        return "No installed apps found"
    headers = ["Name", "Version", "Release", "Codename", "Description"]
    rows = [headers] + [app_package.to_list() for app_package in app_packages]
    return "\n".join([",".join(row) for row in rows])


class UpdatePackageResponse(pydantic.BaseModel):
    updates: list[AppPackage]
    installed_apps: list[AppPackage]
    os: str
    vm_id: str
    warnings: list[str]
    errors: list[str]

    def to_dict(self) -> dict:
        return {
            "updates": [update.to_dict() for update in self.updates],
            "installed_apps": [app.to_dict() for app in self.installed_apps],
            "os": self.os,
            "vm_id": self.vm_id,
            "warnings": self.warnings,
            "errors": self.errors,
        }

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def has_warnings(self) -> bool:
        return len(self.warnings) > 0

    def has_updates(self) -> bool:
        return len(self.updates) > 0

    def has_installed_apps(self) -> bool:
        return len(self.installed_apps) > 0

    def to_string(self) -> str:
        result = f"OS: {self.os}\nVM ID: {self.vm_id}\nWarnings: {self.warnings}\nErrors: {self.errors}"
        if self.has_updates():
            result += f"\nUpdates: {updates_to_string(self.updates)}"
        if self.has_installed_apps():
            result += f"\nInstalled Apps: {updates_to_string(self.installed_apps)}"
        return result

    def installed_apps_to_json(self) -> str:
        if len(self.installed_apps) == 0:
            return "No installed apps found"
        return json.dumps([app.to_dict() for app in self.installed_apps])

    def updates_to_json(self) -> str:
        if len(self.updates) == 0:
            return "No updates found"
        return json.dumps([update.to_dict() for update in self.updates])

    def to_json(self) -> str:
        if len(self.updates) == 0 and len(self.installed_apps) == 0:
            return "No updates or installed apps found"
        return json.dumps(self.to_dict())
