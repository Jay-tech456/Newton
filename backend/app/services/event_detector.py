"""
Event detection service.
Analyzes telemetry data to detect scenario events.
"""
import pandas as pd
from typing import List, Dict, Any
from app.models.event import EventType


class EventDetectorService:
    """
    Detects scenario events from telemetry data using rule-based heuristics.
    
    Detection rules:
    - CUT_IN: cut_in_flag == 1
    - PEDESTRIAN: pedestrian_flag == 1
    - ADVERSE_WEATHER: weather != 'clear'
    - CLOSE_FOLLOWING: lead_distance_m < 15.0
    - SUDDEN_BRAKE: ego_speed_mps drops > 5 m/s within 1 second
    - LANE_CHANGE: ego_yaw changes > 10 degrees within 2 seconds
    """
    
    def __init__(self):
        self.min_event_duration = 0.5  # seconds
        self.close_following_threshold = 15.0  # meters
        self.sudden_brake_threshold = 5.0  # m/s drop
        self.lane_change_yaw_threshold = 10.0  # degrees
    
    def detect_events(self, telemetry_df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Detect all events from telemetry dataframe.
        
        Returns:
            List of event dictionaries with metadata
        """
        events = []
        
        # Detect cut-in events
        events.extend(self._detect_flag_events(
            telemetry_df, 
            'cut_in_flag', 
            EventType.CUT_IN,
            "Vehicle cut-in detected"
        ))
        
        # Detect pedestrian events
        events.extend(self._detect_flag_events(
            telemetry_df, 
            'pedestrian_flag', 
            EventType.PEDESTRIAN,
            "Pedestrian detected"
        ))
        
        # Detect adverse weather
        events.extend(self._detect_adverse_weather(telemetry_df))
        
        # Detect close following
        events.extend(self._detect_close_following(telemetry_df))
        
        # Detect sudden braking
        events.extend(self._detect_sudden_brake(telemetry_df))
        
        # Detect lane changes
        events.extend(self._detect_lane_change(telemetry_df))
        
        # Sort events by timestamp
        events.sort(key=lambda x: x['start_timestamp'])
        
        return events
    
    def _detect_flag_events(
        self, 
        df: pd.DataFrame, 
        flag_column: str, 
        event_type: EventType,
        description: str
    ) -> List[Dict[str, Any]]:
        """Detect events based on binary flag column"""
        events = []
        
        # Find sequences where flag is 1
        flag_series = df[flag_column] == 1
        
        # Find start and end of each sequence
        start_indices = df.index[flag_series & ~flag_series.shift(1, fill_value=False)]
        end_indices = df.index[flag_series & ~flag_series.shift(-1, fill_value=False)]
        
        for start_idx, end_idx in zip(start_indices, end_indices):
            start_row = df.loc[start_idx]
            end_row = df.loc[end_idx]
            
            # Check minimum duration
            duration = end_row['timestamp'] - start_row['timestamp']
            if duration >= self.min_event_duration:
                events.append({
                    'event_type': event_type,
                    'start_frame_id': start_row['frame_id'],
                    'end_frame_id': end_row['frame_id'],
                    'start_timestamp': float(start_row['timestamp']),
                    'end_timestamp': float(end_row['timestamp']),
                    'ego_speed_mps': float(start_row['ego_speed_mps']),
                    'road_type': start_row['road_type'],
                    'weather': start_row['weather'],
                    'lead_distance_m': float(start_row['lead_distance_m']) if pd.notna(start_row['lead_distance_m']) else None,
                    'cut_in_flag': bool(start_row['cut_in_flag']),
                    'pedestrian_flag': bool(start_row['pedestrian_flag']),
                    'description': description,
                    'severity': self._calculate_severity(start_row)
                })
        
        return events
    
    def _detect_adverse_weather(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Detect adverse weather conditions"""
        events = []
        
        # Find sequences where weather is not 'clear'
        adverse_weather = df['weather'] != 'clear'
        
        start_indices = df.index[adverse_weather & ~adverse_weather.shift(1, fill_value=False)]
        end_indices = df.index[adverse_weather & ~adverse_weather.shift(-1, fill_value=False)]
        
        for start_idx, end_idx in zip(start_indices, end_indices):
            start_row = df.loc[start_idx]
            end_row = df.loc[end_idx]
            
            duration = end_row['timestamp'] - start_row['timestamp']
            if duration >= self.min_event_duration:
                events.append({
                    'event_type': EventType.ADVERSE_WEATHER,
                    'start_frame_id': start_row['frame_id'],
                    'end_frame_id': end_row['frame_id'],
                    'start_timestamp': float(start_row['timestamp']),
                    'end_timestamp': float(end_row['timestamp']),
                    'ego_speed_mps': float(start_row['ego_speed_mps']),
                    'road_type': start_row['road_type'],
                    'weather': start_row['weather'],
                    'lead_distance_m': float(start_row['lead_distance_m']) if pd.notna(start_row['lead_distance_m']) else None,
                    'cut_in_flag': bool(start_row['cut_in_flag']),
                    'pedestrian_flag': bool(start_row['pedestrian_flag']),
                    'description': f"Adverse weather: {start_row['weather']}",
                    'severity': 'high' if start_row['weather'] in ['heavy_rain', 'snow', 'fog'] else 'medium'
                })
        
        return events
    
    def _detect_close_following(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Detect close following scenarios"""
        events = []
        
        # Find sequences where lead distance < threshold
        close_following = df['lead_distance_m'] < self.close_following_threshold
        
        start_indices = df.index[close_following & ~close_following.shift(1, fill_value=False)]
        end_indices = df.index[close_following & ~close_following.shift(-1, fill_value=False)]
        
        for start_idx, end_idx in zip(start_indices, end_indices):
            start_row = df.loc[start_idx]
            end_row = df.loc[end_idx]
            
            duration = end_row['timestamp'] - start_row['timestamp']
            if duration >= self.min_event_duration:
                events.append({
                    'event_type': EventType.CLOSE_FOLLOWING,
                    'start_frame_id': start_row['frame_id'],
                    'end_frame_id': end_row['frame_id'],
                    'start_timestamp': float(start_row['timestamp']),
                    'end_timestamp': float(end_row['timestamp']),
                    'ego_speed_mps': float(start_row['ego_speed_mps']),
                    'road_type': start_row['road_type'],
                    'weather': start_row['weather'],
                    'lead_distance_m': float(start_row['lead_distance_m']),
                    'cut_in_flag': bool(start_row['cut_in_flag']),
                    'pedestrian_flag': bool(start_row['pedestrian_flag']),
                    'description': f"Close following: {start_row['lead_distance_m']:.1f}m",
                    'severity': 'high' if start_row['lead_distance_m'] < 10.0 else 'medium'
                })
        
        return events
    
    def _detect_sudden_brake(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Detect sudden braking events"""
        events = []
        
        # Calculate speed change
        df['speed_change'] = df['ego_speed_mps'].diff()
        
        # Find sudden drops in speed
        for i in range(1, len(df)):
            if df.loc[i, 'speed_change'] < -self.sudden_brake_threshold:
                # Found sudden brake
                start_row = df.loc[i-1]
                end_row = df.loc[i]
                
                events.append({
                    'event_type': EventType.SUDDEN_BRAKE,
                    'start_frame_id': start_row['frame_id'],
                    'end_frame_id': end_row['frame_id'],
                    'start_timestamp': float(start_row['timestamp']),
                    'end_timestamp': float(end_row['timestamp']),
                    'ego_speed_mps': float(start_row['ego_speed_mps']),
                    'road_type': start_row['road_type'],
                    'weather': start_row['weather'],
                    'lead_distance_m': float(start_row['lead_distance_m']) if pd.notna(start_row['lead_distance_m']) else None,
                    'cut_in_flag': bool(start_row['cut_in_flag']),
                    'pedestrian_flag': bool(start_row['pedestrian_flag']),
                    'description': f"Sudden brake: {abs(df.loc[i, 'speed_change']):.1f} m/s deceleration",
                    'severity': 'high'
                })
        
        return events
    
    def _detect_lane_change(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Detect lane change events"""
        events = []
        
        # Calculate yaw change over 2-second window
        window_size = 20  # Assuming 10 Hz sampling rate
        
        for i in range(window_size, len(df)):
            yaw_change = abs(df.loc[i, 'ego_yaw'] - df.loc[i-window_size, 'ego_yaw'])
            
            if yaw_change > self.lane_change_yaw_threshold:
                start_row = df.loc[i-window_size]
                end_row = df.loc[i]
                
                events.append({
                    'event_type': EventType.LANE_CHANGE,
                    'start_frame_id': start_row['frame_id'],
                    'end_frame_id': end_row['frame_id'],
                    'start_timestamp': float(start_row['timestamp']),
                    'end_timestamp': float(end_row['timestamp']),
                    'ego_speed_mps': float(start_row['ego_speed_mps']),
                    'road_type': start_row['road_type'],
                    'weather': start_row['weather'],
                    'lead_distance_m': float(start_row['lead_distance_m']) if pd.notna(start_row['lead_distance_m']) else None,
                    'cut_in_flag': bool(start_row['cut_in_flag']),
                    'pedestrian_flag': bool(start_row['pedestrian_flag']),
                    'description': f"Lane change: {yaw_change:.1f}° yaw change",
                    'severity': 'low'
                })
        
        return events
    
    def _calculate_severity(self, row: pd.Series) -> str:
        """Calculate event severity based on context"""
        severity_score = 0
        
        # High speed increases severity
        if row['ego_speed_mps'] > 25:  # ~90 km/h
            severity_score += 1
        
        # Close lead distance increases severity
        if pd.notna(row['lead_distance_m']) and row['lead_distance_m'] < 20:
            severity_score += 1
        
        # Adverse weather increases severity
        if row['weather'] != 'clear':
            severity_score += 1
        
        # Multiple flags increase severity
        if row['cut_in_flag'] and row['pedestrian_flag']:
            severity_score += 2
        
        if severity_score >= 3:
            return 'high'
        elif severity_score >= 1:
            return 'medium'
        else:
            return 'low'
