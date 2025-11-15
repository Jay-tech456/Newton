from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DatasetBase(BaseModel):
    name: str
    description: Optional[str] = None


class DatasetCreate(DatasetBase):
    pass


class DatasetResponse(DatasetBase):
    id: int
    upload_path: str
    frames_path: str
    telemetry_path: str
    frame_count: int
    duration_seconds: int
    created_at: datetime
    
    class Config:
        from_attributes = True
        orm_mode = True
