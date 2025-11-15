"""
Autonomous Driving Data Preprocessing Pipeline

A comprehensive pipeline for processing autonomous driving data including:
- Image analysis with YOLO
- CSV telemetry data processing
- Vector database integration with Pinecone
- Multi-agent interface for data interaction
"""

__version__ = "1.0.0"
__author__ = "Autonomous Driving Pipeline Team"

from .main_pipeline import AutonomousDrivingPipeline
from .data_ingestion import DataIngestion
from .image_analysis import ImageAnalyzer
from .vector_database import VectorDatabaseManager
from .agent_interface import MultiAgentInterface

__all__ = [
    'AutonomousDrivingPipeline',
    'DataIngestion', 
    'ImageAnalyzer',
    'VectorDatabaseManager',
    'MultiAgentInterface'
]