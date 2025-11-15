from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any


class GenomeBase(BaseModel):
    lab_name: str
    version: str
    genome_data: Dict[str, Any]
    parent_version: Optional[str] = None
    change_description: Optional[str] = None
    is_active: int = 1


class GenomeCreate(GenomeBase):
    pass


class GenomeResponse(GenomeBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
        orm_mode = True


class GenomeEvolutionResponse(BaseModel):
    """Response showing evolution of a lab's genome over time"""
    lab_name: str
    versions: list[GenomeResponse]
    
    class Config:
        from_attributes = True
        orm_mode = True
