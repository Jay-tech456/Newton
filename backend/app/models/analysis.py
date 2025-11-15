from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    
    # Lab outputs (stored as JSON)
    safety_lab_output = Column(JSON, nullable=False)  # SafetyLab results
    performance_lab_output = Column(JSON, nullable=False)  # PerformanceLab results
    
    # Judge decision
    judge_decision = Column(JSON, nullable=False)  # Winner, scores, reasoning
    
    # Genome versions used
    safety_genome_version = Column(String, nullable=False)
    performance_genome_version = Column(String, nullable=False)
    
    # New genome versions created (if updated)
    new_safety_genome_version = Column(String, nullable=True)
    new_performance_genome_version = Column(String, nullable=True)
    
    # Metadata
    duration_seconds = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    event = relationship("Event", back_populates="analyses")
