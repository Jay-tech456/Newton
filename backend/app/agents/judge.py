"""
Judge Agent
Compares outputs from SafetyLab and PerformanceLab and determines winner.
"""
import json
from typing import Dict, Any
from app.agents.llm_client import llm_client


class JudgeAgent:
    """
    Evaluates and compares outputs from both labs.
    Provides scores, winner, and reasoning.
    """
    
    def judge(
        self, 
        safety_lab_output: Dict[str, Any],
        performance_lab_output: Dict[str, Any],
        event_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Compare lab outputs and determine winner.
        
        Args:
            safety_lab_output: SafetyLab synthesis
            performance_lab_output: PerformanceLab synthesis
            event_data: Original event context
            
        Returns:
            Judge decision with scores and reasoning
        """
        # Build judgment prompt
        prompt = self._build_judgment_prompt(
            safety_lab_output, 
            performance_lab_output, 
            event_data
        )
        
        # Generate judgment using LLM
        response = llm_client.generate(prompt, context={
            "role": "judge",
            "event_data": event_data
        })
        
        # Parse response
        try:
            judgment = json.loads(response)
        except json.JSONDecodeError:
            judgment = self._default_judgment(
                safety_lab_output, 
                performance_lab_output, 
                event_data
            )
        
        return judgment
    
    def _build_judgment_prompt(
        self,
        safety_lab_output: Dict[str, Any],
        performance_lab_output: Dict[str, Any],
        event_data: Dict[str, Any]
    ) -> str:
        """Build judgment prompt"""
        prompt = f"""
You are an impartial judge evaluating research outputs from two labs.

Event Context:
- Type: {event_data.get("event_type", "")}
- Severity: {event_data.get("severity", "")}

SafetyLab Output:
{json.dumps(safety_lab_output, indent=2)}

PerformanceLab Output:
{json.dumps(performance_lab_output, indent=2)}

Evaluate both outputs on:
1. Relevance to the scenario
2. Quality of recommendations
3. Practical applicability
4. Comprehensiveness

Return JSON format:
{{
    "winner": "SafetyLab" or "PerformanceLab" or "Tie",
    "safety_lab_score": 0.0-1.0,
    "performance_lab_score": 0.0-1.0,
    "reasoning": "detailed explanation",
    "safety_lab_strengths": ["strength1", ...],
    "safety_lab_weaknesses": ["weakness1", ...],
    "performance_lab_strengths": ["strength1", ...],
    "performance_lab_weaknesses": ["weakness1", ...],
    "recommendations_for_improvement": {{
        "SafetyLab": ["rec1", ...],
        "PerformanceLab": ["rec1", ...]
    }}
}}
"""
        return prompt
    
    def _default_judgment(
        self,
        safety_lab_output: Dict[str, Any],
        performance_lab_output: Dict[str, Any],
        event_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Fallback default judgment"""
        # Simple heuristic: favor safety for high-severity events
        severity = event_data.get("severity", "medium")
        event_type = event_data.get("event_type", "")
        
        # Calculate scores based on confidence and number of methods
        safety_confidence = safety_lab_output.get("confidence_level", "medium")
        performance_confidence = performance_lab_output.get("confidence_level", "medium")
        
        confidence_scores = {"high": 0.9, "medium": 0.75, "low": 0.6}
        
        safety_score = confidence_scores.get(safety_confidence, 0.75)
        performance_score = confidence_scores.get(performance_confidence, 0.75)
        
        # Adjust based on event severity
        if severity == "high":
            safety_score += 0.1
        elif severity == "low":
            performance_score += 0.1
        
        # Determine winner
        if abs(safety_score - performance_score) < 0.05:
            winner = "Tie"
        elif safety_score > performance_score:
            winner = "SafetyLab"
        else:
            winner = "PerformanceLab"
        
        return {
            "winner": winner,
            "safety_lab_score": min(safety_score, 1.0),
            "performance_lab_score": min(performance_score, 1.0),
            "reasoning": f"For {event_type} with {severity} severity, {winner} provided more relevant recommendations.",
            "safety_lab_strengths": [
                "Strong focus on safety guarantees",
                "Comprehensive failure mode analysis"
            ],
            "safety_lab_weaknesses": [
                "May sacrifice some performance for safety"
            ],
            "performance_lab_strengths": [
                "High-performance methods",
                "Strong benchmark results"
            ],
            "performance_lab_weaknesses": [
                "Less emphasis on edge cases"
            ],
            "recommendations_for_improvement": {
                "SafetyLab": [
                    "Consider performance trade-offs more explicitly",
                    "Include more real-world deployment examples"
                ],
                "PerformanceLab": [
                    "Incorporate more safety analysis",
                    "Address failure modes more thoroughly"
                ]
            }
        }
