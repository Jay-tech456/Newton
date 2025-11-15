"""
Dataset ingestion service.
Handles ZIP extraction, CSV parsing, and storage.
"""
import os
import zipfile
import shutil
import pandas as pd
from pathlib import Path
from typing import Tuple, Optional
from app.config import settings


class DatasetIngestionService:
    def __init__(self):
        self.storage_path = Path(settings.storage_path)
        self.datasets_path = Path(settings.datasets_path)
        self.frames_path = Path(settings.frames_path)
        
        # Ensure directories exist
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.datasets_path.mkdir(parents=True, exist_ok=True)
        self.frames_path.mkdir(parents=True, exist_ok=True)
    
    def ingest_dataset(
        self, 
        zip_file_path: str, 
        dataset_name: str
    ) -> Tuple[str, str, str, int, int]:
        """
        Extract and process uploaded dataset.
        
        Args:
            zip_file_path: Path to uploaded ZIP file
            dataset_name: Name for the dataset
            
        Returns:
            Tuple of (upload_path, frames_path, telemetry_path, frame_count, duration_seconds)
        """
        # Create dataset directory
        dataset_dir = self.datasets_path / dataset_name
        dataset_dir.mkdir(parents=True, exist_ok=True)
        
        # Extract ZIP
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(dataset_dir)
        
        # Find frames directory and telemetry CSV
        frames_dir = self._find_frames_directory(dataset_dir)
        telemetry_csv = self._find_telemetry_csv(dataset_dir)
        
        if not frames_dir:
            raise ValueError("No 'frames' directory found in uploaded ZIP")
        if not telemetry_csv:
            raise ValueError("No 'telemetry.csv' file found in uploaded ZIP")
        
        # Count frames
        frame_files = list(frames_dir.glob("*.jpg")) + list(frames_dir.glob("*.png"))
        frame_count = len(frame_files)
        
        # Parse telemetry to get duration
        df = pd.read_csv(telemetry_csv)
        if len(df) > 0:
            duration_seconds = int(df['timestamp'].max())
        else:
            duration_seconds = 0
        
        return (
            str(dataset_dir),
            str(frames_dir),
            str(telemetry_csv),
            frame_count,
            duration_seconds
        )
    
    def _find_frames_directory(self, dataset_dir: Path) -> Optional[Path]:
        """Find frames directory in extracted dataset"""
        # Look for 'frames' directory
        frames_dir = dataset_dir / "frames"
        if frames_dir.exists() and frames_dir.is_dir():
            return frames_dir
        
        # Search recursively
        for path in dataset_dir.rglob("frames"):
            if path.is_dir():
                return path
        
        return None
    
    def _find_telemetry_csv(self, dataset_dir: Path) -> Optional[Path]:
        """Find telemetry.csv in extracted dataset"""
        # Look for 'telemetry.csv' in root
        telemetry_csv = dataset_dir / "telemetry.csv"
        if telemetry_csv.exists():
            return telemetry_csv
        
        # Search recursively
        for path in dataset_dir.rglob("telemetry.csv"):
            if path.is_file():
                return path
        
        return None
    
    def validate_telemetry_csv(self, csv_path: str) -> bool:
        """
        Validate that telemetry CSV has required columns.
        
        Required columns:
        - frame_id
        - timestamp
        - ego_speed_mps
        - ego_yaw
        - road_type
        - weather
        - lead_distance_m
        - cut_in_flag
        - pedestrian_flag
        """
        required_columns = [
            'frame_id', 'timestamp', 'ego_speed_mps', 'ego_yaw',
            'road_type', 'weather', 'lead_distance_m',
            'cut_in_flag', 'pedestrian_flag'
        ]
        
        try:
            df = pd.read_csv(csv_path)
            missing_columns = set(required_columns) - set(df.columns)
            
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            return True
        except Exception as e:
            raise ValueError(f"Invalid telemetry CSV: {str(e)}")
    
    def get_telemetry_dataframe(self, csv_path: str) -> pd.DataFrame:
        """Load telemetry CSV as pandas DataFrame"""
        return pd.read_csv(csv_path)
    
    def cleanup_dataset(self, dataset_path: str):
        """Remove dataset directory and all its contents"""
        if os.path.exists(dataset_path):
            shutil.rmtree(dataset_path)
