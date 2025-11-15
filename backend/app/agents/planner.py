"""
Planner Agent
Generates research plan and sub-questions based on scenario and strategy genome.
"""
import json
from typing import Dict, Any, List
from app.agents.llm_client import llm_client


class PlannerAgent:
    """
    Generates research plan for a given scenario event.
    Different labs have different planning priorities based on their genomes.
    """
    
    def __init__(self, lab_name: str, genome: Dict[str, Any]):
        self.lab_name = lab_name
        self.genome = genome
    
    def plan(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate research plan for the event.
        
        Args:
            event_data: Event metadata (type, context, severity, etc.)
            
        Returns:
            Research plan with sub-questions and search strategy
        """
        # Build prompt based on genome and event
        prompt = self._build_planning_prompt(event_data)
        
        # Generate plan using LLM
        response = llm_client.generate(prompt, context={
            "lab_name": self.lab_name,
            "genome": self.genome
        })
        
        # Parse response
        try:
            plan = json.loads(response)
        except json.JSONDecodeError:
            # Fallback to default plan
            plan = self._default_plan(event_data)
        
        return {
            "lab_name": self.lab_name,
            "event_type": event_data.get("event_type"),
            "sub_questions": plan.get("sub_questions", []),
            "search_strategy": plan.get("search_strategy", ""),
            "keywords": self._extract_keywords(event_data),
            "priority_dimensions": self._get_priority_dimensions()
        }
    
    def _build_planning_prompt(self, event_data: Dict[str, Any]) -> str:
        """Build planning prompt based on genome preferences"""
        event_type = event_data.get("event_type", "unknown")
        severity = event_data.get("severity", "medium")
        weather = event_data.get("weather", "clear")
        
        genome_keywords = self.genome.get("retrieval_preferences", {}).get("keywords", [])
        critique_dimensions = self.genome.get("critique_focus", {}).get("dimensions", [])
        
        prompt = f"""
You are a research planner for {self.lab_name}.

Event Context:
- Type: {event_type}
- Severity: {severity}
- Weather: {weather}

Lab Focus Areas: {', '.join(genome_keywords)}
Evaluation Dimensions: {', '.join(critique_dimensions)}

Generate a research plan with 3-5 specific sub-questions to investigate for this scenario.
Focus on {self.lab_name}'s priorities.

Return JSON format:
{{
    "sub_questions": ["question1", "question2", ...],
    "search_strategy": "brief strategy description"
}}
"""
        return prompt
    
    def _extract_keywords(self, event_data: Dict[str, Any]) -> List[str]:
        """Extract relevant keywords from event and genome"""
        keywords = list(self.genome.get("retrieval_preferences", {}).get("keywords", []))
        
        # Add event-specific keywords
        event_type = event_data.get("event_type", "")
        if event_type:
            keywords.append(event_type.replace("_", " "))
        
        weather = event_data.get("weather", "")
        if weather and weather != "clear":
            keywords.append(weather)
        
        return keywords
    
    def _get_priority_dimensions(self) -> List[str]:
        """Get priority evaluation dimensions from genome"""
        return self.genome.get("critique_focus", {}).get("dimensions", [])
    
    def _default_plan(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback default plan if LLM fails"""
        event_type = event_data.get("event_type", "unknown")
        
        if self.lab_name == "SafetyLab":
            return {
                "sub_questions": [
                    f"What are the safety-critical aspects of {event_type} scenarios?",
                    "What robust methods exist for handling this scenario?",
                    "What are the failure modes and mitigation strategies?"
                ],
                "search_strategy": "Focus on safety verification and robustness"
            }
        else:
            return {
                "sub_questions": [
                    f"What are the SOTA methods for {event_type} scenarios?",
                    "How can we optimize performance for this scenario?",
                    "What are the benchmark results for similar scenarios?"
                ],
                "search_strategy": "Focus on performance and efficiency"
            }
