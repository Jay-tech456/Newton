"""
Critic Agent
Evaluates papers based on genome's critique focus dimensions.
"""
import json
from typing import Dict, Any, List
from app.agents.llm_client import llm_client


class CriticAgent:
    """
    Critiques and scores papers based on lab-specific evaluation dimensions.
    """
    
    def __init__(self, lab_name: str, genome: Dict[str, Any]):
        self.lab_name = lab_name
        self.genome = genome
    
    def critique(self, papers: List[Dict[str, Any]], event_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Evaluate papers based on critique dimensions.
        
        Args:
            papers: Papers with extracted info from ReaderAgent
            event_data: Original event context
            
        Returns:
            Papers with critique scores and analysis
        """
        dimensions = self.genome.get("critique_focus", {}).get("dimensions", [])
        weights = self.genome.get("critique_focus", {}).get("weights", {})
        
        critiqued_papers = []
        for paper in papers:
            critique_result = self._critique_paper(paper, dimensions, weights, event_data)
            paper["critique"] = critique_result
            critiqued_papers.append(paper)
        
        # Sort by overall score
        critiqued_papers.sort(key=lambda x: x["critique"]["overall_score"], reverse=True)
        
        return critiqued_papers
    
    def _critique_paper(
        self, 
        paper: Dict[str, Any], 
        dimensions: List[str], 
        weights: Dict[str, float],
        event_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Critique a single paper.
        """
        # Build critique prompt
        prompt = self._build_critique_prompt(paper, dimensions, event_data)
        
        # Generate critique using LLM
        response = llm_client.generate(prompt, context={
            "lab_name": self.lab_name,
            "genome": self.genome
        })
        
        # Parse response
        try:
            critique = json.loads(response)
        except json.JSONDecodeError:
            critique = self._default_critique(paper, dimensions)
        
        # Calculate overall score
        scores = critique.get("scores", {})
        overall_score = sum(scores.get(dim, 0.5) * weights.get(dim, 1.0) for dim in dimensions)
        weight_sum = sum(weights.get(dim, 1.0) for dim in dimensions)
        
        # Avoid division by zero
        if weight_sum > 0:
            overall_score /= weight_sum
        else:
            overall_score = 0.5  # Default score if no weights
        
        critique["overall_score"] = overall_score
        
        return critique
    
    def _build_critique_prompt(
        self, 
        paper: Dict[str, Any], 
        dimensions: List[str],
        event_data: Dict[str, Any]
    ) -> str:
        """Build critique prompt"""
        title = paper.get("title", "")
        extracted_info = paper.get("extracted_info", {})
        
        prompt = f"""
You are a research critic for {self.lab_name}.

Paper: {title}
Method Category: {paper.get("method_category", "")}

Event Context:
- Type: {event_data.get("event_type", "")}
- Severity: {event_data.get("severity", "")}

Extracted Information:
{json.dumps(extracted_info, indent=2)}

Evaluate this paper on the following dimensions: {', '.join(dimensions)}

Return JSON format:
{{
    "scores": {{"dimension1": 0.0-1.0, "dimension2": 0.0-1.0, ...}},
    "strengths": ["strength1", "strength2", ...],
    "weaknesses": ["weakness1", "weakness2", ...]
}}
"""
        return prompt
    
    def _default_critique(self, paper: Dict[str, Any], dimensions: List[str]) -> Dict[str, Any]:
        """Fallback default critique"""
        # Simple heuristic scoring based on available data
        scores = {}
        extracted_info = paper.get("extracted_info", {})
        
        for dim in dimensions:
            if dim == "robustness":
                metrics = extracted_info.get("robustness_metrics", {})
                if metrics.get("detection_accuracy_rain"):
                    scores[dim] = metrics["detection_accuracy_rain"]
                else:
                    scores[dim] = 0.7
            
            elif dim == "accuracy":
                metrics = extracted_info.get("performance_metrics", {})
                if metrics.get("accuracy"):
                    scores[dim] = metrics["accuracy"]
                else:
                    scores[dim] = 0.75
            
            elif dim == "speed":
                metrics = extracted_info.get("performance_metrics", {})
                fps = metrics.get("fps", 30)
                scores[dim] = min(fps / 60.0, 1.0)  # Normalize to 60 FPS
            
            elif dim == "computational_efficiency":
                metrics = extracted_info.get("computational_cost", {})
                fps = metrics.get("fps", 30)
                scores[dim] = min(fps / 60.0, 1.0)
            
            else:
                scores[dim] = 0.75  # Default score
        
        return {
            "scores": scores,
            "strengths": ["Well-documented methodology", "Clear experimental results"],
            "weaknesses": ["Limited real-world validation"]
        }
