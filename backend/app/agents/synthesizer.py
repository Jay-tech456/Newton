"""
Synthesizer Agent
Synthesizes research findings into actionable recommendations.
"""
import json
from typing import Dict, Any, List
from app.agents.llm_client import llm_client


class SynthesizerAgent:
    """
    Synthesizes research findings into a coherent report.
    """
    
    def __init__(self, lab_name: str, genome: Dict[str, Any]):
        self.lab_name = lab_name
        self.genome = genome
    
    def synthesize(
        self, 
        research_plan: Dict[str, Any],
        papers: List[Dict[str, Any]], 
        event_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Synthesize research findings into recommendations.
        
        Args:
            research_plan: Original research plan
            papers: Critiqued papers from CriticAgent
            event_data: Original event context
            
        Returns:
            Synthesis report with recommendations
        """
        synthesis_style = self.genome.get("synthesis_style", {})
        
        # Build synthesis prompt
        prompt = self._build_synthesis_prompt(research_plan, papers, event_data, synthesis_style)
        
        # Generate synthesis using LLM
        response = llm_client.generate(prompt, context={
            "lab_name": self.lab_name,
            "genome": self.genome
        })
        
        # Parse response
        try:
            synthesis = json.loads(response)
        except json.JSONDecodeError:
            synthesis = self._default_synthesis(papers, event_data)
        
        # Add metadata
        synthesis["lab_name"] = self.lab_name
        synthesis["event_type"] = event_data.get("event_type")
        synthesis["num_papers_analyzed"] = len(papers)
        synthesis["top_papers"] = [
            {
                "title": p["title"],
                "score": p["critique"]["overall_score"],
                "method_category": p.get("method_category", "")
            }
            for p in papers[:3]
        ]
        
        return synthesis
    
    def _build_synthesis_prompt(
        self,
        research_plan: Dict[str, Any],
        papers: List[Dict[str, Any]],
        event_data: Dict[str, Any],
        synthesis_style: Dict[str, Any]
    ) -> str:
        """Build synthesis prompt"""
        audience = synthesis_style.get("audience", "engineers")
        emphasis = synthesis_style.get("emphasis", "balanced")
        
        # Summarize top papers
        top_papers_summary = []
        for paper in papers[:5]:
            top_papers_summary.append({
                "title": paper["title"],
                "score": paper["critique"]["overall_score"],
                "strengths": paper["critique"].get("strengths", []),
                "weaknesses": paper["critique"].get("weaknesses", [])
            })
        
        prompt = f"""
You are a research synthesizer for {self.lab_name}.

Event Context:
- Type: {event_data.get("event_type", "")}
- Severity: {event_data.get("severity", "")}

Research Questions:
{json.dumps(research_plan.get("sub_questions", []), indent=2)}

Top Papers Analyzed:
{json.dumps(top_papers_summary, indent=2)}

Audience: {audience}
Emphasis: {emphasis}

Synthesize the research findings into actionable recommendations.

Return JSON format:
{{
    "summary": "brief overview",
    "key_methods": ["method1", "method2", ...],
    "deployment_recommendations": ["rec1", "rec2", ...],
    "trade_offs": {{"aspect": "description"}},
    "confidence_level": "high/medium/low"
}}
"""
        return prompt
    
    def _default_synthesis(self, papers: List[Dict[str, Any]], event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback default synthesis"""
        top_papers = papers[:3]
        
        key_methods = []
        deployment_recs = []
        
        for paper in top_papers:
            method_name = paper.get("extracted_info", {}).get("method_name", paper["title"])
            key_methods.append(method_name)
            
            deployment_notes = paper.get("extracted_info", {}).get("deployment_notes", "")
            if deployment_notes:
                deployment_recs.append(deployment_notes)
        
        if self.lab_name == "SafetyLab":
            summary = f"For {event_data.get('event_type', 'this scenario')}, prioritize methods with strong safety guarantees and robustness."
            trade_offs = {
                "safety_vs_performance": "Higher safety guarantees may reduce performance",
                "complexity_vs_reliability": "More complex verification increases reliability but adds overhead"
            }
        else:
            summary = f"For {event_data.get('event_type', 'this scenario')}, prioritize high-performance methods with real-time capability."
            trade_offs = {
                "performance_vs_safety": "Higher performance may sacrifice some safety guarantees",
                "accuracy_vs_speed": "Faster inference may reduce accuracy slightly"
            }
        
        return {
            "summary": summary,
            "key_methods": key_methods,
            "deployment_recommendations": deployment_recs if deployment_recs else ["Conduct thorough testing before deployment"],
            "trade_offs": trade_offs,
            "confidence_level": "medium"
        }
