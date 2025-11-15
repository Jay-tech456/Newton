"""
Forethought Integration (Stub)
Simulates ingesting incident tickets or support reports related to driving failures.
"""
from typing import List, Dict, Any
from datetime import datetime, timedelta
import random


class ForethoughtIncidentService:
    """
    Stub service for Forethought incident integration.
    Simulates incident reports that can inform Meta-Learner priorities.
    """
    
    def __init__(self, api_key: str = None, enabled: bool = False):
        self.api_key = api_key
        self.enabled = enabled
    
    def get_recent_incidents(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        Get recent incident reports (mock data).
        
        Args:
            days: Number of days to look back
            
        Returns:
            List of incident reports
        """
        if not self.enabled:
            return []
        
        # Mock incident data
        incident_types = [
            "adverse_weather_failure",
            "cut_in_collision",
            "pedestrian_near_miss",
            "sensor_occlusion",
            "planning_timeout",
            "false_positive_brake"
        ]
        
        severities = ["critical", "high", "medium", "low"]
        
        incidents = []
        for i in range(random.randint(5, 15)):
            incident_date = datetime.now() - timedelta(days=random.randint(0, days))
            
            incidents.append({
                "incident_id": f"INC-{1000 + i}",
                "type": random.choice(incident_types),
                "severity": random.choice(severities),
                "description": f"Mock incident report for {random.choice(incident_types)}",
                "reported_at": incident_date.isoformat(),
                "affected_users": random.randint(1, 100),
                "resolution_status": random.choice(["open", "investigating", "resolved"])
            })
        
        return incidents
    
    def get_incident_patterns(self) -> Dict[str, Any]:
        """
        Analyze incident patterns to inform research priorities.
        
        Returns:
            Pattern analysis with recommendations
        """
        if not self.enabled:
            return {
                "enabled": False,
                "message": "Forethought integration not enabled"
            }
        
        incidents = self.get_recent_incidents()
        
        # Count incidents by type
        type_counts = {}
        for incident in incidents:
            incident_type = incident["type"]
            type_counts[incident_type] = type_counts.get(incident_type, 0) + 1
        
        # Find most common issues
        sorted_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "enabled": True,
            "total_incidents": len(incidents),
            "incident_breakdown": type_counts,
            "top_issues": [t[0] for t in sorted_types[:3]],
            "recommendations": {
                "research_focus": [
                    f"Increase research emphasis on {sorted_types[0][0]}" if sorted_types else "No specific recommendations",
                    "Consider adding keywords related to top incident types",
                    "Adjust genome weights to prioritize robustness in failure-prone scenarios"
                ]
            }
        }
    
    def should_adjust_genome_for_incidents(self, lab_name: str) -> Dict[str, Any]:
        """
        Determine if genome should be adjusted based on incident patterns.
        
        Args:
            lab_name: Lab to check adjustments for
            
        Returns:
            Adjustment recommendations
        """
        patterns = self.get_incident_patterns()
        
        if not patterns.get("enabled"):
            return {"should_adjust": False}
        
        top_issues = patterns.get("top_issues", [])
        
        if not top_issues:
            return {"should_adjust": False}
        
        # SafetyLab should focus more on high-incident areas
        if lab_name == "SafetyLab":
            return {
                "should_adjust": True,
                "reason": f"High incident rate in {top_issues[0]}",
                "suggested_keywords": [issue.replace("_", " ") for issue in top_issues],
                "suggested_weight_increase": {
                    "robustness": 0.1,
                    "failure_recovery": 0.1
                }
            }
        
        return {"should_adjust": False}


# Global instance
forethought_service = ForethoughtIncidentService(enabled=False)
