import pydantic


class Os(pydantic.BaseModel):
    name: str
    version: str
    codename: str
    release: str

    def __str__(self):
        return f"{self.name} {self.version} {self.codename} {self.release}"


def os_to_string(os: Os) -> str:
    return f"{os.name} {os.version} {os.codename} {os.release}"
