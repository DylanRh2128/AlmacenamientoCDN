from datetime import datetime

from pydantic import BaseModel


class FileOut(BaseModel):
    id: int
    created_at: datetime
    original_filename: str
    content_type: str
    size_bytes: int

    model_config = {"from_attributes": True}


class DownloadUrlOut(BaseModel):
    url: str
    expires_in_seconds: int
