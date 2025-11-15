from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class Dataset(Base):
    __tablename__ = "datasets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    upload_path = Column(String, nullable=False)  # Path to extracted dataset
    frames_path = Column(String, nullable=False)  # Path to frames directory
    telemetry_path = Column(String, nullable=False)  # Path to telemetry CSV
    frame_count = Column(Integer, default=0)
    duration_seconds = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    events = relationship("Event", back_populates="dataset", cascade="all, delete-orphan")
