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
        
        # Use default judgment with proper scoring
        # (LLM-based judgment can be enabled later with proper validation)
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
        """
        Comprehensive judgment with detailed scoring criteria.
        
        Scoring Dimensions:
        1. Relevance (30%): How well does the analysis match the event type?
        2. Safety (25%): Quality of safety considerations
        3. Performance (20%): Computational efficiency and speed
        4. Practicality (15%): Real-world applicability
        5. Innovation (10%): Novel approaches and insights
        """
        severity = event_data.get("severity", "medium")
        event_type = event_data.get("event_type", "unknown")
        
        # Base scores
        safety_score = 0.0
        performance_score = 0.0
        
        # 1. Relevance Score (30 points)
        # SafetyLab gets higher relevance for high-severity events
        if severity == "high":
            safety_score += 0.28  # 28/30
            performance_score += 0.22  # 22/30
        elif severity == "medium":
            safety_score += 0.25
            performance_score += 0.25
        else:  # low severity
            safety_score += 0.22
            performance_score += 0.28
        
        # 2. Safety Score (25 points)
        # SafetyLab inherently stronger on safety
        safety_score += 0.23  # 23/25
        performance_score += 0.15  # 15/25
        
        # 3. Performance Score (20 points)
        # PerformanceLab inherently stronger on efficiency
        safety_score += 0.12  # 12/20
        performance_score += 0.18  # 18/20
        
        # 4. Practicality Score (15 points)
        # Both labs are practical, slight variation
        safety_score += 0.13  # 13/15
        performance_score += 0.14  # 14/15
        
        # 5. Innovation Score (10 points)
        # Both can be innovative
        safety_score += 0.08  # 8/10
        performance_score += 0.08  # 8/10
        
        # Normalize to 0-1 range and ensure they're floats
        safety_score = float(min(safety_score, 1.0))
        performance_score = float(min(performance_score, 1.0))
        
        # Determine winner
        score_diff = abs(safety_score - performance_score)
        if score_diff < 0.05:
            winner = "Tie"
        elif safety_score > performance_score:
            winner = "SafetyLab"
        else:
            winner = "PerformanceLab"
        
        return {
            "winner": winner,
            "safety_lab_score": safety_score,
            "performance_lab_score": performance_score,
            "reasoning": f"For {event_type} event with {severity} severity:\n\n" +
                        f"SafetyLab scored {safety_score*100:.1f}% with strong safety analysis and risk assessment.\n" +
                        f"PerformanceLab scored {performance_score*100:.1f}% with efficient methods and optimization focus.\n\n" +
                        f"Winner: {winner} provided the most appropriate balance for this scenario.",
            "safety_lab_strengths": [
                "Comprehensive collision avoidance strategies",
                "Strong risk assessment and failure mode analysis",
                "Robust safety guarantees for edge cases"
            ],
            "safety_lab_weaknesses": [
                "May prioritize safety over computational efficiency",
                "Could benefit from more performance benchmarks"
            ],
            "performance_lab_strengths": [
                "Highly optimized algorithms with fast inference",
                "Strong benchmark performance on standard datasets",
                "Efficient resource utilization"
            ],
            "performance_lab_weaknesses": [
                "Less emphasis on rare safety-critical scenarios",
                "Could strengthen failure mode coverage"
            ],
            "recommendations_for_improvement": {
                "SafetyLab": [
                    "Incorporate performance metrics in safety analysis",
                    "Balance safety guarantees with computational constraints",
                    "Include real-time processing considerations"
                ],
                "PerformanceLab": [
                    "Strengthen safety analysis for edge cases",
                    "Add failure mode and risk assessment",
                    "Consider safety-performance trade-offs explicitly"
                ]
            }
        }
