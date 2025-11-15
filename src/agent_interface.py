"""
Multi-Agent Interface for Autonomous Driving Data
Provides structured access for agents to interact with processed driving data
"""

import json
import logging
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from datetime import datetime
from src.main_pipeline import AutonomousDrivingPipeline

logger = logging.getLogger(__name__)

@dataclass
class AgentQuery:
    """Standardized query format for agents"""
    query_type: str  # 'search', 'filter', 'analysis', 'temporal'
    parameters: Dict[str, Any]
    agent_id: str
    timestamp: str

@dataclass
class AgentResponse:
    """Standardized response format for agents"""
    success: bool
    data: Any
    metadata: Dict[str, Any]
    error_message: Optional[str] = None
    response_time_ms: Optional[float] = None

class MultiAgentInterface:
    """Interface for multi-agent systems to interact with autonomous driving data"""
    
    def __init__(self, pipeline: AutonomousDrivingPipeline):
        self.pipeline = pipeline
        self.query_history = []
        self.agent_sessions = {}
        
        logger.info("Multi-Agent Interface initialized")
    
    def handle_agent_query(self, agent_id: str, query: Dict) -> AgentResponse:
        """
        Handle query from an agent
        
        Args:
            agent_id: Unique identifier for the agent
            query: Query dictionary with standardized format
            
        Returns:
            AgentResponse with results or error
        """
        start_time = datetime.now()
        
        try:
            # Parse query
            agent_query = self._parse_query(agent_id, query)
            
            # Execute query based on type
            result = self._execute_query(agent_query)
            
            # Calculate response time
            response_time = (datetime.now() - start_time).total_seconds() * 1000
            
            # Create response
            response = AgentResponse(
                success=True,
                data=result,
                metadata={
                    'agent_id': agent_id,
                    'query_type': agent_query.query_type,
                    'timestamp': agent_query.timestamp,
                    'result_count': len(result) if isinstance(result, list) else 1
                },
                response_time_ms=response_time
            )
            
            # Log query
            self._log_query(agent_id, agent_query, response)
            
            return response
            
        except Exception as e:
            response_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return AgentResponse(
                success=False,
                data=None,
                metadata={'agent_id': agent_id, 'error_type': type(e).__name__},
                error_message=str(e),
                response_time_ms=response_time
            )
    
    def _parse_query(self, agent_id: str, query: Dict) -> AgentQuery:
        """Parse and validate agent query"""
        required_fields = ['query_type', 'parameters']
        
        for field in required_fields:
            if field not in query:
                raise ValueError(f"Missing required field: {field}")
        
        return AgentQuery(
            query_type=query['query_type'],
            parameters=query['parameters'],
            agent_id=agent_id,
            timestamp=datetime.now().isoformat()
        )
    
    def _execute_query(self, query: AgentQuery) -> Any:
        """Execute query based on type"""
        query_type = query.query_type.lower()
        
        if query_type == 'search':
            return self._handle_search_query(query.parameters)
        elif query_type == 'filter':
            return self._handle_filter_query(query.parameters)
        elif query_type == 'analysis':
            return self._handle_analysis_query(query.parameters)
        elif query_type == 'temporal':
            return self._handle_temporal_query(query.parameters)
        elif query_type == 'stats':
            return self._handle_stats_query(query.parameters)
        else:
            raise ValueError(f"Unsupported query type: {query_type}")
    
    def _handle_search_query(self, params: Dict) -> List[Dict]:
        """Handle semantic search queries"""
        query_text = params.get('text', '')
        top_k = params.get('limit', 10)
        filters = params.get('filters', {})
        
        if not query_text:
            raise ValueError("Search query requires 'text' parameter")
        
        return self.pipeline.search_frames(query_text, top_k, filters)
    
    def _handle_filter_query(self, params: Dict) -> List[Dict]:
        """Handle filtering queries"""
        filter_type = params.get('filter_type', '')
        
        if filter_type == 'risk_level':
            risk_level = params.get('level', 'high')
            limit = params.get('limit', 50)
            return self.pipeline.get_high_risk_frames(limit) if risk_level == 'high' else \
                   self.pipeline.vector_db.get_frames_by_risk_level(risk_level, limit)
        
        elif filter_type == 'tags':
            tags = params.get('tags', [])
            limit = params.get('limit', 50)
            if not isinstance(tags, list):
                tags = [tags]
            return self.pipeline.get_frames_by_situation(tags, limit)
        
        elif filter_type == 'telemetry':
            return self._filter_by_telemetry(params)
        
        else:
            raise ValueError(f"Unsupported filter type: {filter_type}")
    
    def _handle_analysis_query(self, params: Dict) -> Dict:
        """Handle analysis queries"""
        analysis_type = params.get('analysis_type', '')
        
        if analysis_type == 'summary':
            return self._generate_summary_analysis(params)
        elif analysis_type == 'risk_assessment':
            return self._generate_risk_assessment(params)
        elif analysis_type == 'pattern_detection':
            return self._detect_patterns(params)
        else:
            raise ValueError(f"Unsupported analysis type: {analysis_type}")
    
    def _handle_temporal_query(self, params: Dict) -> List[Dict]:
        """Handle temporal/spatial queries"""
        # This would require timestamp-based filtering
        # For now, return all frames with temporal ordering
        query_text = f"temporal sequence frames"
        results = self.pipeline.search_frames(query_text, top_k=params.get('limit', 100))
        
        # Sort by timestamp if available
        if results:
            results.sort(key=lambda x: x.get('metadata', {}).get('timestamp', 0))
        
        return results
    
    def _handle_stats_query(self, params: Dict) -> Dict:
        """Handle statistics queries"""
        stats_type = params.get('stats_type', 'pipeline')
        
        if stats_type == 'pipeline':
            return self.pipeline.get_pipeline_stats()
        elif stats_type == 'database':
            return self.pipeline.vector_db.get_index_stats()
        elif stats_type == 'agent_usage':
            return self._get_agent_usage_stats()
        else:
            raise ValueError(f"Unsupported stats type: {stats_type}")
    
    def _filter_by_telemetry(self, params: Dict) -> List[Dict]:
        """Filter frames based on telemetry conditions"""
        conditions = params.get('conditions', {})
        limit = params.get('limit', 50)
        
        # Build query text based on conditions
        query_parts = []
        
        if 'speed_range' in conditions:
            speed_min, speed_max = conditions['speed_range']
            query_parts.append(f"speed between {speed_min} and {speed_max} m/s")
        
        if 'road_types' in conditions:
            road_types = conditions['road_types']
            if isinstance(road_types, list):
                query_parts.append(f"road types {', '.join(road_types)}")
            else:
                query_parts.append(f"road type {road_types}")
        
        if 'weather_conditions' in conditions:
            weather = conditions['weather_conditions']
            if isinstance(weather, list):
                query_parts.append(f"weather {', '.join(weather)}")
            else:
                query_parts.append(f"weather {weather}")
        
        if 'distance_threshold' in conditions:
            threshold = conditions['distance_threshold']
            query_parts.append(f"lead distance less than {threshold} meters")
        
        query_text = ". ".join(query_parts) if query_parts else "all frames"
        
        return self.pipeline.search_frames(query_text, limit)
    
    def _generate_summary_analysis(self, params: Dict) -> Dict:
        """Generate summary analysis of dataset"""
        # Get sample frames for analysis
        sample_frames = self.pipeline.search_frames("sample frames", top_k=100)
        
        if not sample_frames:
            return {"error": "No frames found for analysis"}
        
        # Analyze sample
        analysis = {
            'total_sampled': len(sample_frames),
            'road_type_distribution': {},
            'weather_distribution': {},
            'risk_level_distribution': {},
            'average_speed': 0,
            'common_objects': {},
            'high_risk_situations': []
        }
        
        speeds = []
        
        for frame in sample_frames:
            metadata = frame.get('metadata', {})
            
            # Road types
            road_type = metadata.get('telemetry', {}).get('road_type', 'unknown')
            analysis['road_type_distribution'][road_type] = \
                analysis['road_type_distribution'].get(road_type, 0) + 1
            
            # Weather
            weather = metadata.get('telemetry', {}).get('weather', 'unknown')
            analysis['weather_distribution'][weather] = \
                analysis['weather_distribution'].get(weather, 0) + 1
            
            # Risk levels
            risk_level = metadata.get('risk_level', 'unknown')
            analysis['risk_level_distribution'][risk_level] = \
                analysis['risk_level_distribution'].get(risk_level, 0) + 1
            
            # Speed
            speed = metadata.get('telemetry', {}).get('ego_speed_mps', 0)
            speeds.append(speed)
            
            # Common objects
            search_tags = metadata.get('search_tags', [])
            for tag in search_tags:
                if tag in ['car', 'person', 'truck', 'bus', 'motorcycle']:
                    analysis['common_objects'][tag] = \
                        analysis['common_objects'].get(tag, 0) + 1
            
            # High risk situations
            if risk_level in ['high', 'medium']:
                analysis['high_risk_situations'].append({
                    'frame_id': metadata.get('frame_id'),
                    'risk_level': risk_level,
                    'situation': search_tags[:3]  # Top 3 tags
                })
        
        # Calculate averages
        if speeds:
            analysis['average_speed'] = sum(speeds) / len(speeds)
        
        return analysis
    
    def _generate_risk_assessment(self, params: Dict) -> Dict:
        """Generate risk assessment report"""
        high_risk_frames = self.pipeline.get_high_risk_frames(top_k=50)
        medium_risk_frames = self.pipeline.vector_db.get_frames_by_risk_level('medium', 50)
        
        return {
            'high_risk_count': len(high_risk_frames),
            'medium_risk_count': len(medium_risk_frames),
            'high_risk_samples': high_risk_frames[:5],  # Sample of 5
            'risk_factors': self._analyze_risk_factors(high_risk_frames + medium_risk_frames),
            'recommendations': self._generate_safety_recommendations()
        }
    
    def _detect_patterns(self, params: Dict) -> Dict:
        """Detect patterns in the driving data"""
        patterns = {
            'frequent_situations': {},
            'temporal_patterns': {},
            'correlations': {}
        }
        
        # Get frames for pattern analysis
        frames = self.pipeline.search_frames("pattern analysis", top_k=200)
        
        # Analyze frequent situations
        all_tags = []
        for frame in frames:
            tags = frame.get('metadata', {}).get('search_tags', [])
            all_tags.extend(tags)
        
        # Count tag frequency
        tag_counts = {}
        for tag in all_tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        # Get top patterns
        patterns['frequent_situations'] = dict(
            sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        )
        
        return patterns
    
    def _analyze_risk_factors(self, frames: List[Dict]) -> List[Dict]:
        """Analyze common risk factors"""
        risk_factors = {}
        
        for frame in frames:
            metadata = frame.get('metadata', {})
            tags = metadata.get('search_tags', [])
            telemetry = metadata.get('telemetry', {})
            
            # Analyze contributing factors
            for tag in tags:
                if tag in ['cut_in', 'pedestrian', 'high_speed', 'rainy', 'urban']:
                    risk_factors[tag] = risk_factors.get(tag, 0) + 1
            
            # Speed-related risks
            speed = telemetry.get('ego_speed_mps', 0)
            if speed > 30:  # High speed
                risk_factors['high_speed'] = risk_factors.get('high_speed', 0) + 1
        
        return sorted(
            [{'factor': k, 'count': v} for k, v in risk_factors.items()],
            key=lambda x: x['count'],
            reverse=True
        )
    
    def _generate_safety_recommendations(self) -> List[str]:
        """Generate safety recommendations based on analysis"""
        recommendations = [
            "Implement adaptive cruise control for cut-in situations",
            "Enhance pedestrian detection in urban environments",
            "Reduce speed in adverse weather conditions",
            "Improve lane keeping assistance on highways",
            "Add warning systems for close vehicle following"
        ]
        
        return recommendations
    
    def _get_agent_usage_stats(self) -> Dict:
        """Get agent usage statistics"""
        return {
            'total_queries': len(self.query_history),
            'active_agents': len(self.agent_sessions),
            'query_types': self._get_query_type_distribution(),
            'average_response_time_ms': self._get_average_response_time()
        }
    
    def _get_query_type_distribution(self) -> Dict[str, int]:
        """Get distribution of query types"""
        distribution = {}
        for query in self.query_history:
            query_type = query.get('query_type', 'unknown')
            distribution[query_type] = distribution.get(query_type, 0) + 1
        return distribution
    
    def _get_average_response_time(self) -> float:
        """Calculate average response time"""
        if not self.query_history:
            return 0.0
        
        response_times = [
            query.get('response_time_ms', 0) 
            for query in self.query_history 
            if 'response_time_ms' in query
        ]
        
        return sum(response_times) / len(response_times) if response_times else 0.0
    
    def _log_query(self, agent_id: str, query: AgentQuery, response: AgentResponse):
        """Log query for analytics"""
        log_entry = {
            'agent_id': agent_id,
            'query_type': query.query_type,
            'parameters': query.parameters,
            'timestamp': query.timestamp,
            'success': response.success,
            'response_time_ms': response.response_time_ms,
            'result_count': response.metadata.get('result_count', 0)
        }
        
        self.query_history.append(log_entry)
        
        # Update agent session
        if agent_id not in self.agent_sessions:
            self.agent_sessions[agent_id] = {
                'first_query': query.timestamp,
                'last_query': query.timestamp,
                'query_count': 0
            }
        
        self.agent_sessions[agent_id]['last_query'] = query.timestamp
        self.agent_sessions[agent_id]['query_count'] += 1
    
    def get_agent_capabilities(self) -> Dict:
        """Get available agent capabilities"""
        return {
            'query_types': [
                {
                    'type': 'search',
                    'description': 'Semantic search for similar frames',
                    'parameters': ['text', 'limit', 'filters']
                },
                {
                    'type': 'filter',
                    'description': 'Filter frames by criteria',
                    'parameters': ['filter_type', 'conditions', 'limit']
                },
                {
                    'type': 'analysis',
                    'description': 'Analyze driving patterns and risks',
                    'parameters': ['analysis_type', 'conditions']
                },
                {
                    'type': 'temporal',
                    'description': 'Get temporal sequences of frames',
                    'parameters': ['limit', 'time_range']
                },
                {
                    'type': 'stats',
                    'description': 'Get pipeline and database statistics',
                    'parameters': ['stats_type']
                }
            ],
            'filter_options': {
                'risk_levels': ['minimal', 'low', 'medium', 'high'],
                'common_tags': ['car', 'person', 'truck', 'bus', 'cut_in', 'pedestrian', 'high_speed'],
                'road_types': ['highway', 'urban', 'rural'],
                'weather_conditions': ['clear', 'rainy', 'foggy', 'cloudy']
            }
        }

# Example usage functions for agents
def create_safety_agent(pipeline: AutonomousDrivingPipeline) -> Dict:
    """Create a safety-focused agent query interface"""
    interface = MultiAgentInterface(pipeline)
    
    def safety_query(query_text: str):
        return interface.handle_agent_query(
            agent_id="safety_agent",
            query={
                "query_type": "search",
                "parameters": {
                    "text": query_text,
                    "filters": {"risk_level": {"$ne": "minimal"}},
                    "limit": 20
                }
            }
        )
    
    return {
        "query": safety_query,
        "get_high_risk": lambda: interface.handle_agent_query(
            "safety_agent",
            {"query_type": "filter", "parameters": {"filter_type": "risk_level", "level": "high"}}
        ),
        "risk_assessment": lambda: interface.handle_agent_query(
            "safety_agent",
            {"query_type": "analysis", "parameters": {"analysis_type": "risk_assessment"}}
        )
    }

def create_analysis_agent(pipeline: AutonomousDrivingPipeline) -> Dict:
    """Create an analysis-focused agent interface"""
    interface = MultiAgentInterface(pipeline)
    
    def analyze_situation(situation: str):
        return interface.handle_agent_query(
            agent_id="analysis_agent",
            query={
                "query_type": "search",
                "parameters": {
                    "text": f"situations with {situation}",
                    "limit": 50
                }
            }
        )
    
    return {
        "analyze": analyze_situation,
        "get_patterns": lambda: interface.handle_agent_query(
            "analysis_agent",
            {"query_type": "analysis", "parameters": {"analysis_type": "pattern_detection"}}
        ),
        "get_summary": lambda: interface.handle_agent_query(
            "analysis_agent",
            {"query_type": "analysis", "parameters": {"analysis_type": "summary"}}
        )
    }