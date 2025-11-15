"""
Vector Database Integration Module for Autonomous Driving Pipeline
Handles Pinecone integration and embedding generation
"""

import pinecone
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import json
from datetime import datetime
import os

logger = logging.getLogger(__name__)

@dataclass
class VectorRecord:
    """Record for storing in vector database"""
    id: str
    vector: List[float]
    metadata: Dict[str, Any]
    text_content: str

class VectorDatabaseManager:
    """Manages vector database operations using Pinecone"""
    
    def __init__(self, config: dict):
        self.config = config
        self.pinecone_config = config['pinecone']
        self.embedding_config = config['embeddings']
        
        # Initialize Pinecone
        self.pc = Pinecone(
            api_key=self.pinecone_config['api_key']
        )

        # Initialize embedding model
        self.embedding_model = SentenceTransformer(
            self.embedding_config['model_name'],
            device=self.embedding_config['device']
        )

        self.index_name = self.pinecone_config['index_name']
        self.batch_size = self.pinecone_config['batch_size']

        # Initialize index
        self._initialize_index()
        
        logger.info(f"Initialized vector database: {self.index_name}")
    
    def _initialize_index(self):
        """Initialize Pinecone index"""
        # Check if index exists
        if self.index_name not in self.pc.list_indexes().names():
            logger.info(f"Creating new index: {self.index_name}")
            self.pc.create_index(
                name=self.index_name,
                dimension=self.pinecone_config['dimension'],
                metric=self.pinecone_config['metric']
            )

        # Connect to index
        self.index = self.pc.Index(self.index_name)

        # Get index stats
        stats = self.index.describe_index_stats()
        logger.info(f"Index stats: {stats}")
    
    def process_and_store_frames(self, frames: Dict[str, Dict]) -> List[str]:
        """
        Process frames and store in vector database
        
        Args:
            frames: Dictionary of frame_id -> frame_data
            
        Returns:
            List of stored vector IDs
        """
        logger.info(f"Processing {len(frames)} frames for vector storage")
        
        vector_records = []
        
        for frame_id, frame_data in frames.items():
            try:
                # Create text representation for embedding
                text_content = self._create_text_representation(frame_data)
                
                # Generate embedding
                embedding = self._generate_embedding(text_content)
                
                # Create comprehensive metadata
                metadata = self._create_metadata(frame_data)
                
                # Create vector record
                record = VectorRecord(
                    id=f"frame_{frame_id}_{int(datetime.now().timestamp())}",
                    vector=embedding.tolist(),
                    metadata=metadata,
                    text_content=text_content
                )
                
                vector_records.append(record)
                
            except Exception as e:
                logger.error(f"Error processing frame {frame_id}: {e}")
                continue
        
        # Store in batches
        stored_ids = []
        for i in range(0, len(vector_records), self.batch_size):
            batch = vector_records[i:i + self.batch_size]
            batch_ids = self._store_batch(batch)
            stored_ids.extend(batch_ids)
        
        logger.info(f"Stored {len(stored_ids)} vectors in database")
        return stored_ids
    
    def _create_text_representation(self, frame_data: Dict) -> str:
        """Create comprehensive text representation for embedding"""
        telemetry = frame_data.get('telemetry', {})
        image_analysis = frame_data.get('image_analysis')
        
        # Build text description
        text_parts = []
        
        # Telemetry information
        text_parts.append(f"Frame {frame_data['frame_id']} at timestamp {telemetry.get('timestamp', 0)}")
        text_parts.append(f"Vehicle speed: {telemetry.get('ego_speed_mps', 0)} m/s")
        text_parts.append(f"Vehicle yaw: {telemetry.get('ego_yaw', 0)}")
        text_parts.append(f"Road type: {telemetry.get('road_type', 'unknown')}")
        text_parts.append(f"Weather: {telemetry.get('weather', 'unknown')}")
        text_parts.append(f"Lead vehicle distance: {telemetry.get('lead_distance_m', 0)} meters")
        
        # Event flags
        if telemetry.get('cut_in_flag', False):
            text_parts.append("Cut-in maneuver detected")
        
        if telemetry.get('pedestrian_flag', False):
            text_parts.append("Pedestrian detected by telemetry")
        
        # Image analysis if available
        if image_analysis:
            # Detections
            if image_analysis.detections:
                detected_objects = []
                for detection in image_analysis.detections:
                    detected_objects.append(f"{detection.class_name} (confidence: {detection.confidence:.2f})")
                
                if detected_objects:
                    text_parts.append(f"Detected objects: {', '.join(detected_objects)}")
            
            # Scene information
            text_parts.append(f"Weather assessment: {image_analysis.weather_assessment}")
            text_parts.append(f"Visibility score: {image_analysis.visibility_score:.2f}")
            text_parts.append(f"Obstacle count: {image_analysis.obstacle_count}")
            text_parts.append(f"Risk level: {image_analysis.risk_level}")
            
            # Lane information
            lane_info = image_analysis.lane_info
            text_parts.append(f"Lane lines detected: {lane_info['lines_detected']}")
            if lane_info['lines_detected']:
                text_parts.append(f"Lane confidence: {lane_info['lane_confidence']:.2f}")
        
        # Combine all parts
        return ". ".join(text_parts)
    
    def _generate_embedding(self, text: str) -> np.ndarray:
        """Generate text embedding using sentence transformer"""
        try:
            embedding = self.embedding_model.encode(
                text,
                batch_size=self.embedding_config['batch_size'],
                show_progress_bar=False
            )
            return embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            # Return zero vector as fallback
            return np.zeros(self.embedding_model.get_sentence_embedding_dimension())
    
    def _create_metadata(self, frame_data: Dict) -> Dict[str, Any]:
        """Create comprehensive metadata for vector storage"""
        telemetry = frame_data.get('telemetry', {})
        image_analysis = frame_data.get('image_analysis')
        
        metadata = {
            # Frame identification
            'frame_id': frame_data['frame_id'],
            'timestamp': frame_data['timestamp'],
            'processing_timestamp': datetime.now().isoformat(),
            
            # Telemetry data
            'telemetry': {
                'ego_speed_mps': float(telemetry.get('ego_speed_mps', 0)),
                'ego_yaw': float(telemetry.get('ego_yaw', 0)),
                'road_type': telemetry.get('road_type', 'unknown'),
                'weather': telemetry.get('weather', 'unknown'),
                'lead_distance_m': float(telemetry.get('lead_distance_m', 0)),
                'cut_in_flag': bool(telemetry.get('cut_in_flag', False)),
                'pedestrian_flag': bool(telemetry.get('pedestrian_flag', False))
            },
            
            # Image analysis results
            'image_analysis': None,
            'detections_summary': {
                'total_objects': 0,
                'vehicles': 0,
                'pedestrians': 0,
                'other_objects': 0
            },
            
            # Search-friendly tags
            'search_tags': [],
            'risk_level': 'unknown',
            'visibility_score': 0.0,
            'has_image': frame_data.get('image_path') is not None
        }
        
        # Add image analysis if available
        if image_analysis:
            metadata['image_analysis'] = {
                'weather_assessment': image_analysis.weather_assessment,
                'visibility_score': float(image_analysis.visibility_score),
                'obstacle_count': image_analysis.obstacle_count,
                'risk_level': image_analysis.risk_level,
                'lane_info': image_analysis.lane_info
            }
            
            # Summarize detections
            if image_analysis.detections:
                detection_summary = {'total_objects': len(image_analysis.detections)}
                class_counts = {}
                
                for detection in image_analysis.detections:
                    class_name = detection.class_name
                    class_counts[class_name] = class_counts.get(class_name, 0) + 1
                
                detection_summary.update(class_counts)
                metadata['detections_summary'] = detection_summary
                
                # Create search tags
                metadata['search_tags'] = list(class_counts.keys())
                if image_analysis.risk_level != 'minimal':
                    metadata['search_tags'].append('high_risk')
                if image_analysis.obstacle_count > 5:
                    metadata['search_tags'].append('crowded')
            
            metadata['risk_level'] = image_analysis.risk_level
            metadata['visibility_score'] = float(image_analysis.visibility_score)
        
        # Add additional search tags based on telemetry
        if telemetry.get('cut_in_flag', False):
            metadata['search_tags'].append('cut_in')
        
        if telemetry.get('pedestrian_flag', False):
            metadata['search_tags'].append('pedestrian')
        
        if telemetry.get('ego_speed_mps', 0) > 25:
            metadata['search_tags'].append('high_speed')
        
        road_type = telemetry.get('road_type', '')
        if road_type:
            metadata['search_tags'].append(road_type)
        
        weather = telemetry.get('weather', '')
        if weather:
            metadata['search_tags'].append(weather)
        
        return metadata
    
    def _store_batch(self, records: List[VectorRecord]) -> List[str]:
        """Store a batch of records in Pinecone"""
        try:
            # Prepare batch data
            batch_data = []
            ids = []
            
            for record in records:
                batch_data.append({
                    'id': record.id,
                    'values': record.vector,
                    'metadata': record.metadata
                })
                ids.append(record.id)
            
            # Upsert to Pinecone
            self.index.upsert(vectors=batch_data)
            
            logger.debug(f"Stored batch of {len(records)} vectors")
            return ids
            
        except Exception as e:
            logger.error(f"Error storing batch: {e}")
            return []
    
    def search_similar_frames(self, query_text: str, top_k: int = 10, 
                            filters: Optional[Dict] = None) -> List[Dict]:
        """
        Search for similar frames using text query
        
        Args:
            query_text: Text query for similarity search
            top_k: Number of results to return
            filters: Optional metadata filters
            
        Returns:
            List of similar frames with metadata
        """
        try:
            # Generate query embedding
            query_embedding = self._generate_embedding(query_text)
            
            # Prepare search request
            search_args = {
                'vector': query_embedding.tolist(),
                'top_k': top_k,
                'include_metadata': True
            }
            
            # Add filters if provided
            if filters:
                search_args['filter'] = filters
            
            # Perform search
            results = self.index.query(**search_args)
            
            # Process results
            similar_frames = []
            for match in results['matches']:
                similar_frames.append({
                    'id': match['id'],
                    'score': match['score'],
                    'metadata': match['metadata']
                })
            
            return similar_frames
            
        except Exception as e:
            logger.error(f"Error searching frames: {e}")
            return []
    
    def get_frames_by_risk_level(self, risk_level: str, top_k: int = 100) -> List[Dict]:
        """Get frames filtered by risk level"""
        filters = {'risk_level': risk_level}
        return self.search_similar_frames(
            query_text=f"frames with {risk_level} risk level",
            top_k=top_k,
            filters=filters
        )
    
    def get_frames_by_tags(self, tags: List[str], top_k: int = 100) -> List[Dict]:
        """Get frames filtered by search tags"""
        filters = {'search_tags': {'$in': tags}}
        return self.search_similar_frames(
            query_text=f"frames with tags: {', '.join(tags)}",
            top_k=top_k,
            filters=filters
        )
    
    def delete_frame(self, frame_id: str) -> bool:
        """Delete a specific frame from the database"""
        try:
            # Find vectors with matching frame_id
            # Note: This would require storing frame_id in metadata and using metadata filtering
            # For now, we'll need to implement a more sophisticated deletion strategy
            logger.warning("Frame deletion not fully implemented - requires metadata filtering")
            return False
        except Exception as e:
            logger.error(f"Error deleting frame {frame_id}: {e}")
            return False
    
    def get_index_stats(self) -> Dict:
        """Get current index statistics"""
        try:
            return self.index.describe_index_stats()
        except Exception as e:
            logger.error(f"Error getting index stats: {e}")
            return {}
