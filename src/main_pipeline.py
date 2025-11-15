"""
Main Pipeline for Autonomous Driving Data Processing
Orchestrates the entire preprocessing workflow
"""

import os
import yaml
import logging
from pathlib import Path
from typing import Dict, List, Optional
from dotenv import load_dotenv
import time
from datetime import datetime

from src.data_ingestion import DataIngestion, IngestedData
from src.image_analysis import ImageAnalyzer
from src.vector_database import VectorDatabaseManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AutonomousDrivingPipeline:
    """Main pipeline for processing autonomous driving data"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize the pipeline with configuration"""
        self.config = self._load_config(config_path)
        self._setup_directories()
        self._initialize_components()
        
        # Pipeline statistics
        self.stats = {
            'total_frames_processed': 0,
            'total_images_analyzed': 0,
            'total_vectors_stored': 0,
            'processing_time_total': 0,
            'pipeline_start_time': datetime.now()
        }
        
        logger.info("Autonomous Driving Pipeline initialized")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            # Load environment variables
            load_dotenv()
            
            # Replace environment variables in config
            config = self._replace_env_vars(config)
            
            return config
            
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            raise
    
    def _replace_env_vars(self, config: Dict) -> Dict:
        """Replace ${VAR} patterns with environment variables"""
        import re
        
        def replace_recursive(obj):
            if isinstance(obj, dict):
                return {k: replace_recursive(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [replace_recursive(item) for item in obj]
            elif isinstance(obj, str):
                # Replace ${VAR} patterns
                pattern = r'\$\{([^}]+)\}'
                def env_replacer(match):
                    var_name = match.group(1)
                    return os.getenv(var_name, match.group(0))
                return re.sub(pattern, env_replacer, obj)
            else:
                return obj
        
        return replace_recursive(config)
    
    def _setup_directories(self):
        """Create necessary directories"""
        directories = [
            self.config['data']['input_dir'],
            self.config['data']['output_dir'],
            self.config['data']['temp_dir']
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    def _initialize_components(self):
        """Initialize pipeline components"""
        try:
            # Initialize data ingestion
            self.data_ingestion = DataIngestion(self.config)
            
            # Initialize image analyzer
            self.image_analyzer = ImageAnalyzer(self.config)
            
            # Initialize vector database manager
            self.vector_db = VectorDatabaseManager(self.config)
            
            logger.info("All components initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing components: {e}")
            raise
    
    def process_zip_file(self, zip_path: str) -> Dict:
        """
        Process a complete .zip file containing images and CSV data
        
        Args:
            zip_path: Path to the .zip file
            
        Returns:
            Processing results and statistics
        """
        logger.info(f"Starting processing of zip file: {zip_path}")
        start_time = time.time()
        
        try:
            # Step 1: Ingest data
            logger.info("Step 1: Ingesting data from zip file")
            ingested_data = self.data_ingestion.process_zip_file(zip_path)
            
            # Step 2: Analyze images
            logger.info("Step 2: Analyzing images with YOLO")
            frames_with_analysis = self._analyze_all_images(ingested_data.frames)
            
            # Step 3: Generate embeddings and store in vector database
            logger.info("Step 3: Generating embeddings and storing in vector database")
            stored_vector_ids = self.vector_db.process_and_store_frames(frames_with_analysis)
            
            # Step 4: Generate processing report
            processing_time = time.time() - start_time
            results = self._generate_processing_report(
                ingested_data, stored_vector_ids, processing_time
            )
            
            # Update statistics
            self._update_stats(results)
            
            logger.info(f"Processing completed in {processing_time:.2f} seconds")
            return results
            
        except Exception as e:
            logger.error(f"Error processing zip file: {e}")
            raise
    
    def process_csv_file(self, csv_path: str, image_dir: str = None) -> Dict:
        """
        Process CSV file with optional image directory
        
        Args:
            csv_path: Path to CSV file
            image_dir: Optional directory containing images
            
        Returns:
            Processing results
        """
        logger.info(f"Processing CSV file: {csv_path}")
        start_time = time.time()
        
        try:
            # Process CSV data
            csv_data = self.data_ingestion.process_csv_file(csv_path)
            
            # Create frame structure
            frames = {}
            for _, row in csv_data.iterrows():
                frame_id = str(int(row['frame_id']))
                
                # Try to find matching image
                image_path = None
                if image_dir:
                    for ext in ['.jpg', '.jpeg', '.png', '.bmp']:
                        potential_path = os.path.join(image_dir, f"{frame_id}{ext}")
                        if os.path.exists(potential_path):
                            image_path = potential_path
                            break
                
                frames[frame_id] = {
                    'frame_id': frame_id,
                    'timestamp': row['timestamp'],
                    'telemetry': row.to_dict(),
                    'image_path': image_path,
                    'image_analysis': None,
                    'vector_embedding': None
                }
            
            # Analyze images and store in vector database
            frames_with_analysis = self._analyze_all_images(frames)
            stored_vector_ids = self.vector_db.process_and_store_frames(frames_with_analysis)
            
            # Generate results
            processing_time = time.time() - start_time
            ingested_data = IngestedData(
                frames=frames_with_analysis,
                csv_data=csv_data,
                image_files=[f['image_path'] for f in frames_with_analysis.values() if f['image_path']],
                metadata={'source_file': csv_path, 'image_dir': image_dir}
            )
            
            results = self._generate_processing_report(
                ingested_data, stored_vector_ids, processing_time
            )
            
            self._update_stats(results)
            return results
            
        except Exception as e:
            logger.error(f"Error processing CSV file: {e}")
            raise
    
    def process_mock_data(self, num_frames: int = 10) -> Dict:
        """Process mock data for testing purposes"""
        logger.info(f"Processing {num_frames} frames of mock data")
        
        try:
            # Generate mock data
            ingested_data = self.data_ingestion.generate_mock_data(num_frames)
            
            # Simulate image analysis (without actual images)
            frames_with_analysis = self._simulate_image_analysis(ingested_data.frames)
            
            # Store in vector database
            stored_vector_ids = self.vector_db.process_and_store_frames(frames_with_analysis)
            
            # Generate results
            processing_time = 0.1  # Simulated processing time
            results = self._generate_processing_report(
                ingested_data, stored_vector_ids, processing_time
            )
            
            self._update_stats(results)
            return results
            
        except Exception as e:
            logger.error(f"Error processing mock data: {e}")
            raise
    
    def _analyze_all_images(self, frames: Dict[str, Dict]) -> Dict[str, Dict]:
        """Analyze images for all frames"""
        frames_with_analysis = frames.copy()
        analyzed_count = 0
        
        for frame_id, frame_data in frames.items():
            if frame_data.get('image_path') and os.path.exists(frame_data['image_path']):
                try:
                    # Perform image analysis
                    analysis = self.image_analyzer.analyze_image(
                        frame_data['image_path'], 
                        frame_data.get('telemetry', {})
                    )
                    frames_with_analysis[frame_id]['image_analysis'] = analysis
                    analyzed_count += 1
                    
                except Exception as e:
                    logger.warning(f"Error analyzing frame {frame_id}: {e}")
                    frames_with_analysis[frame_id]['image_analysis'] = None
            else:
                frames_with_analysis[frame_id]['image_analysis'] = None
        
        logger.info(f"Analyzed {analyzed_count} images")
        return frames_with_analysis
    
    def _simulate_image_analysis(self, frames: Dict[str, Dict]) -> Dict[str, Dict]:
        """Simulate image analysis for mock data"""
        from src.image_analysis import SceneAnalysis, DetectionResult
        
        frames_with_analysis = frames.copy()
        
        for frame_id, frame_data in frames.items():
            telemetry = frame_data.get('telemetry', {})
            
            # Create mock detections based on telemetry
            mock_detections = []
            
            if telemetry.get('pedestrian_flag', False):
                mock_detections.append(DetectionResult(
                    class_name='person',
                    confidence=0.85,
                    bbox=[100, 100, 150, 200],
                    center=(125, 150),
                    area=2500
                ))
            
            if telemetry.get('cut_in_flag', False):
                mock_detections.append(DetectionResult(
                    class_name='car',
                    confidence=0.92,
                    bbox=[300, 150, 450, 250],
                    center=(375, 200),
                    area=15000
                ))
            
            # Create mock scene analysis
            mock_analysis = SceneAnalysis(
                detections=mock_detections,
                lane_info={'lines_detected': True, 'line_count': 2, 'lane_width_estimate': 45.0, 'lane_confidence': 0.8},
                weather_assessment=telemetry.get('weather', 'clear'),
                visibility_score=0.85,
                obstacle_count=len(mock_detections),
                risk_level='medium' if telemetry.get('cut_in_flag', False) else 'low',
                depth_estimates={d.class_name: {'distance_category': '20-50m', 'bbox_area_ratio': 0.05, 'confidence': d.confidence} for d in mock_detections}
            )
            
            frames_with_analysis[frame_id]['image_analysis'] = mock_analysis
        
        return frames_with_analysis
    
    def _generate_processing_report(self, ingested_data: IngestedData, 
                                  stored_vector_ids: List[str], processing_time: float) -> Dict:
        """Generate comprehensive processing report"""
        total_frames = len(ingested_data.frames)
        frames_with_images = sum(1 for f in ingested_data.frames.values() if f.get('image_path'))
        frames_analyzed = sum(1 for f in ingested_data.frames.values() if f.get('image_analysis'))
        
        return {
            'processing_summary': {
                'total_frames': total_frames,
                'frames_with_images': frames_with_images,
                'frames_analyzed': frames_analyzed,
                'vectors_stored': len(stored_vector_ids),
                'processing_time_seconds': processing_time,
                'frames_per_second': total_frames / processing_time if processing_time > 0 else 0
            },
            'ingestion_metadata': ingested_data.metadata,
            'stored_vector_ids': stored_vector_ids,
            'pipeline_stats': self.stats,
            'timestamp': datetime.now().isoformat()
        }
    
    def _update_stats(self, results: Dict):
        """Update pipeline statistics"""
        summary = results['processing_summary']
        
        self.stats['total_frames_processed'] += summary['total_frames']
        self.stats['total_images_analyzed'] += summary['frames_analyzed']
        self.stats['total_vectors_stored'] += summary['vectors_stored']
        self.stats['processing_time_total'] += summary['processing_time_seconds']
    
    def search_frames(self, query_text: str, top_k: int = 10, 
                     filters: Optional[Dict] = None) -> List[Dict]:
        """Search for similar frames using text query"""
        return self.vector_db.search_similar_frames(query_text, top_k, filters)
    
    def get_high_risk_frames(self, top_k: int = 50) -> List[Dict]:
        """Get high-risk frames from the database"""
        return self.vector_db.get_frames_by_risk_level('high', top_k)
    
    def get_frames_by_situation(self, situation: str, top_k: int = 50) -> List[Dict]:
        """Get frames by specific situation (e.g., 'cut_in', 'pedestrian', 'high_speed')"""
        return self.vector_db.get_frames_by_tags([situation], top_k)
    
    def get_pipeline_stats(self) -> Dict:
        """Get current pipeline statistics"""
        current_time = datetime.now()
        runtime = (current_time - self.stats['pipeline_start_time']).total_seconds()
        
        return {
            **self.stats,
            'pipeline_runtime_seconds': runtime,
            'average_processing_fps': self.stats['total_frames_processed'] / runtime if runtime > 0 else 0,
            'vector_db_stats': self.vector_db.get_index_stats(),
            'last_updated': current_time.isoformat()
        }
    
    def cleanup_temp_files(self):
        """Clean up temporary files"""
        import shutil
        temp_dir = self.config['data']['temp_dir']
        try:
            shutil.rmtree(temp_dir)
            Path(temp_dir).mkdir(parents=True, exist_ok=True)
            logger.info("Temporary files cleaned up")
        except Exception as e:
            logger.warning(f"Error cleaning temp files: {e}")

def main():
    """Example usage of the pipeline"""
    # Initialize pipeline
    pipeline = AutonomousDrivingPipeline()
    
    # Example 1: Process mock data
    print("Processing mock data...")
    results = pipeline.process_mock_data(num_frames=5)
    print(f"Mock data processed: {results['processing_summary']}")
    
    # Example 2: Search for frames
    print("\nSearching for high-risk frames...")
    high_risk_frames = pipeline.get_high_risk_frames(top_k=5)
    print(f"Found {len(high_risk_frames)} high-risk frames")
    
    # Example 3: Get pipeline stats
    print("\nPipeline statistics:")
    stats = pipeline.get_pipeline_stats()
    print(f"Total frames processed: {stats['total_frames_processed']}")
    print(f"Total vectors stored: {stats['total_vectors_stored']}")
    
    # Cleanup
    pipeline.cleanup_temp_files()

if __name__ == "__main__":
    main()