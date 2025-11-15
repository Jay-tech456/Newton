from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from app.db.database import Base


class EventType(str, Enum):
    CUT_IN = "cut_in"
    PEDESTRIAN = "pedestrian"
    ADVERSE_WEATHER = "adverse_weather"
    CLOSE_FOLLOWING = "close_following"
    SUDDEN_BRAKE = "sudden_brake"
    LANE_CHANGE = "lane_change"
    OTHER = "other"


class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    
    # Event metadata
    event_type = Column(SQLEnum(EventType), nullable=False)
    start_frame_id = Column(String, nullable=False)
    end_frame_id = Column(String, nullable=False)
    start_timestamp = Column(Float, nullable=False)
    end_timestamp = Column(Float, nullable=False)
    
    # Scenario context
    ego_speed_mps = Column(Float, nullable=True)
    road_type = Column(String, nullable=True)
    weather = Column(String, nullable=True)
    lead_distance_m = Column(Float, nullable=True)
    
    # Flags
    cut_in_flag = Column(Boolean, default=False)
    pedestrian_flag = Column(Boolean, default=False)
    
    # Additional context
    description = Column(Text, nullable=True)
    severity = Column(String, default="medium")  # low, medium, high
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    dataset = relationship("Dataset", back_populates="events")
    analyses = relationship("Analysis", back_populates="event", cascade="all, delete-orphan")
