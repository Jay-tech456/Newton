from sqlalchemy import Column, Integer, String, DateTime, JSON, Text
from datetime import datetime
from app.db.database import Base


class StrategyGenome(Base):
    __tablename__ = "strategy_genomes"
    
    id = Column(Integer, primary_key=True, index=True)
    lab_name = Column(String, nullable=False, index=True)  # "SafetyLab" or "PerformanceLab"
    version = Column(String, nullable=False, index=True)  # e.g., "v0.1", "v0.2"
    
    # Genome configuration (stored as JSON)
    genome_data = Column(JSON, nullable=False)
    # Structure:
    # {
    #   "retrieval_preferences": {
    #     "year_window": [2018, 2024],
    #     "venue_weights": {"CVPR": 1.0, "ICCV": 1.0, "NeurIPS": 0.8},
    #     "keywords": ["autonomous driving", "perception", "planning"]
    #   },
    #   "reading_template": {
    #     "extract_fields": ["method", "results", "limitations", "deployment_notes"]
    #   },
    #   "critique_focus": {
    #     "dimensions": ["robustness", "rare_events", "safety_metrics"],
    #     "weights": {"robustness": 1.0, "rare_events": 0.9, "safety_metrics": 1.0}
    #   },
    #   "synthesis_style": {
    #     "audience": "safety_engineers",
    #     "max_tokens": 500,
    #     "format": "structured"
    #   }
    # }
    
    # Parent version (for tracking evolution)
    parent_version = Column(String, nullable=True)
    
    # Change description
    change_description = Column(Text, nullable=True)
    
    # Metadata
    is_active = Column(Integer, default=1)  # 1 for active, 0 for archived
    created_at = Column(DateTime, default=datetime.utcnow)
