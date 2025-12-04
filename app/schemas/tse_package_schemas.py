from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, HttpUrl, ConfigDict


class TSEPackageCreate(BaseModel):
    url: HttpUrl
    package_type: str


class TSEPackageResponse(BaseModel):
    id: UUID
    source: str
    dataset: str
    file_name: Optional[str] = None
    raw_data: dict
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
