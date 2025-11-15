from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.event import EventType


class EventBase(BaseModel):
    event_type: EventType
    start_frame_id: str
    end_frame_id: str
    start_timestamp: float
    end_timestamp: float
    ego_speed_mps: Optional[float] = None
    road_type: Optional[str] = None
    weather: Optional[str] = None
    lead_distance_m: Optional[float] = None
    cut_in_flag: bool = False
    pedestrian_flag: bool = False
    description: Optional[str] = None
    severity: str = "medium"


class EventCreate(EventBase):
    dataset_id: int


class EventResponse(EventBase):
    id: int
    dataset_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
        orm_mode = True
