from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any


class AnalysisBase(BaseModel):
    event_id: int
    safety_lab_output: Dict[str, Any]
    performance_lab_output: Dict[str, Any]
    judge_decision: Dict[str, Any]
    safety_genome_version: str
    performance_genome_version: str
    new_safety_genome_version: Optional[str] = None
    new_performance_genome_version: Optional[str] = None
    duration_seconds: Optional[int] = None


class AnalysisCreate(AnalysisBase):
    pass


class AnalysisResponse(AnalysisBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
        orm_mode = True
