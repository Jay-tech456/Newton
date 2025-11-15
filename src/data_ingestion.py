"""
Data Ingestion Module for Autonomous Driving Pipeline
Handles .zip files with images and CSV telemetry data
"""

import os
import zipfile
import pandas as pd
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import chardet
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class IngestedData:
    """Container for ingested data"""
    frames: Dict[str, Dict]  # frame_id -> {image_path, telemetry, metadata}
    csv_data: pd.DataFrame
    image_files: List[str]
    metadata: Dict

class DataIngestion:
    """Handles ingestion of .zip files and CSV data for autonomous driving pipeline"""
    
    def __init__(self, config: dict):
        self.config = config
        self.supported_image_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
        self.required_csv_columns = set(config['csv']['required_columns'])
        
    def process_zip_file(self, zip_path: str) -> IngestedData:
        """
        Process a .zip file containing images and CSV data
        
        Args:
            zip_path: Path to the .zip file
            
        Returns:
            IngestedData object with organized frame data
        """
        logger.info(f"Processing zip file: {zip_path}")
        
        # Extract zip file
        extract_dir = self._extract_zip(zip_path)
        
        # Find and process CSV file
        csv_data = self._find_and_process_csv(extract_dir)
        
        # Find image files
        image_files = self._find_image_files(extract_dir)
        
        # Organize data by frames
        frames = self._organize_frames(csv_data, image_files, extract_dir)
        
        # Create metadata
        metadata = {
            'source_file': zip_path,
            'total_frames': len(frames),
            'image_count': len(image_files),
            'csv_rows': len(csv_data),
            'extract_dir': extract_dir
        }
        
        return IngestedData(
            frames=frames,
            csv_data=csv_data,
            image_files=image_files,
            metadata=metadata
        )
    
    def process_csv_file(self, csv_path: str) -> pd.DataFrame:
        """Process standalone CSV file with telemetry data"""
        logger.info(f"Processing CSV file: {csv_path}")
        
        # Detect encoding
        with open(csv_path, 'rb') as f:
            result = chardet.detect(f.read())
            encoding = result['encoding']
        
        # Read CSV
        try:
            df = pd.read_csv(csv_path, encoding=encoding)
        except UnicodeDecodeError:
            df = pd.read_csv(csv_path, encoding='utf-8')
        
        # Validate columns
        self._validate_csv_columns(df)
        
        # Convert data types
        df = self._convert_csv_dtypes(df)
        
        return df
    
    def _extract_zip(self, zip_path: str) -> str:
        """Extract zip file to temporary directory"""
        extract_dir = os.path.join(
            self.config['data']['temp_dir'],
            f"extract_{Path(zip_path).stem}"
        )
        os.makedirs(extract_dir, exist_ok=True)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        logger.info(f"Extracted to: {extract_dir}")
        return extract_dir
    
    def _find_and_process_csv(self, extract_dir: str) -> pd.DataFrame:
        """Find and process CSV file in extracted directory"""
        csv_files = list(Path(extract_dir).rglob("*.csv"))
        
        if not csv_files:
            raise ValueError("No CSV file found in the zip archive")
        
        # Use the first CSV file found
        csv_path = csv_files[0]
        logger.info(f"Found CSV file: {csv_path}")
        
        return self.process_csv_file(str(csv_path))
    
    def _find_image_files(self, extract_dir: str) -> List[str]:
        """Find all image files in extracted directory"""
        image_files = []
        
        for ext in self.supported_image_formats:
            image_files.extend(Path(extract_dir).rglob(f"*{ext}"))
        
        image_files = [str(f) for f in image_files]
        logger.info(f"Found {len(image_files)} image files")
        
        return image_files
    
    def _organize_frames(self, csv_data: pd.DataFrame, image_files: List[str], extract_dir: str) -> Dict[str, Dict]:
        """Organize data by frame_id"""
        frames = {}
        
        # Process CSV data into frames
        for _, row in csv_data.iterrows():
            frame_id = str(int(row['frame_id']))
            frames[frame_id] = {
                'frame_id': frame_id,
                'timestamp': row['timestamp'],
                'telemetry': row.to_dict(),
                'image_path': None,  # Will be filled if image found
                'image_analysis': None,  # Will be filled later
                'vector_embedding': None  # Will be filled later
            }
        
        # Match image files to frames
        for image_path in image_files:
            # Try to extract frame_id from filename
            filename = Path(image_path).stem
            possible_frame_ids = [
                filename,
                filename.split('_')[-1],  # If format is "image_123"
                filename.split('-')[-1],  # If format is "image-123"
            ]
            
            for possible_id in possible_frame_ids:
                if possible_id.isdigit():
                    frame_id = str(int(possible_id))
                    if frame_id in frames:
                        frames[frame_id]['image_path'] = image_path
                        break
        
        # Log unmatched images
        matched_images = sum(1 for f in frames.values() if f['image_path'])
        logger.info(f"Matched {matched_images}/{len(image_files)} images to frames")
        
        return frames
    
    def _validate_csv_columns(self, df: pd.DataFrame):
        """Validate CSV has required columns"""
        missing_columns = self.required_csv_columns - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
    
    def _convert_csv_dtypes(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert CSV columns to appropriate data types"""
        # Convert frame_id to string
        df['frame_id'] = df['frame_id'].astype(str)
        
        # Convert numeric columns
        numeric_columns = [
            'timestamp', 'ego_speed_mps', 'ego_yaw', 'lead_distance_m'
        ]
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Convert boolean flags
        boolean_columns = ['cut_in_flag', 'pedestrian_flag']
        for col in boolean_columns:
            if col in df.columns:
                df[col] = df[col].astype(bool)
        
        return df
    
    def generate_mock_data(self, num_frames: int = 10) -> IngestedData:
        """Generate mock data for testing purposes"""
        logger.info(f"Generating {num_frames} frames of mock data")
        
        # Generate mock CSV data
        mock_csv_data = []
        for i in range(1, num_frames + 1):
            mock_csv_data.append({
                'frame_id': i,
                'timestamp': i * 0.1,
                'ego_speed_mps': 25.0 + (i % 10),
                'ego_yaw': 0.01 * (i % 5),
                'road_type': 'highway' if i % 2 == 0 else 'urban',
                'weather': 'clear' if i % 3 != 0 else 'rainy',
                'lead_distance_m': 30.0 + (i % 20),
                'cut_in_flag': i % 7 == 0,
                'pedestrian_flag': i % 11 == 0
            })
        
        csv_data = pd.DataFrame(mock_csv_data)
        
        # Create mock frames
        frames = {}
        for _, row in csv_data.iterrows():
            frame_id = str(int(row['frame_id']))
            frames[frame_id] = {
                'frame_id': frame_id,
                'timestamp': row['timestamp'],
                'telemetry': row.to_dict(),
                'image_path': f"mock_images/frame_{frame_id}.jpg",
                'image_analysis': None,
                'vector_embedding': None
            }
        
        # Create metadata
        metadata = {
            'source_file': 'mock_data',
            'total_frames': len(frames),
            'image_count': len(frames),
            'csv_rows': len(csv_data),
            'extract_dir': 'mock'
        }
        
        return IngestedData(
            frames=frames,
            csv_data=csv_data,
            image_files=[f["image_path"] for f in frames.values()],
            metadata=metadata
        )