from pydantic import BaseModel


class GetVmScreenshotResult(BaseModel):
    success: bool
    message: str
    raw_screenshot: bytes | None
    screenshot: str | None
    border_color: str | None
