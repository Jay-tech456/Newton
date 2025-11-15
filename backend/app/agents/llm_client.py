"""
Mock LLM client interface.
Can be replaced with real LLM providers (LiquidMetal AI, MCP Total, OpenAI, etc.)
"""
from typing import Dict, Any
import json


class LLMClient:
    """
    Mock LLM client that generates deterministic responses.
    Replace this with real LLM integration later.
    """
    
    def __init__(self, provider: str = "mock"):
        self.provider = provider
    
    def generate(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """
        Generate text based on prompt.
        
        Args:
            prompt: The prompt text
            context: Optional context dictionary
            
        Returns:
            Generated text
        """
        if self.provider == "mock":
            return self._mock_generate(prompt, context)
        else:
            # Placeholder for real LLM integration
            raise NotImplementedError(f"Provider {self.provider} not implemented")
    
    def _mock_generate(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """
        Generate mock responses based on prompt keywords.
        """
        prompt_lower = prompt.lower()
        
        # Planning responses
        if "research plan" in prompt_lower or "sub-questions" in prompt_lower:
            if "safety" in prompt_lower:
                return json.dumps({
                    "sub_questions": [
                        "What are the latest collision avoidance methods for cut-in scenarios?",
                        "How do robust perception systems handle adverse weather?",
                        "What safety verification techniques exist for autonomous planning?"
                    ],
                    "search_strategy": "Focus on safety-critical methods with proven robustness"
                })
            else:
                return json.dumps({
                    "sub_questions": [
                        "What are the SOTA end-to-end learning methods for autonomous driving?",
                        "How can we optimize real-time performance for perception pipelines?",
                        "What are the latest benchmarks for autonomous driving performance?"
                    ],
                    "search_strategy": "Focus on high-performance methods with strong benchmark results"
                })
        
        # Critique responses
        elif "critique" in prompt_lower or "evaluate" in prompt_lower:
            if "safety" in prompt_lower:
                return json.dumps({
                    "scores": {
                        "robustness": 0.85,
                        "rare_events_handling": 0.78,
                        "safety_metrics": 0.90,
                        "worst_case_performance": 0.75
                    },
                    "strengths": [
                        "Strong theoretical safety guarantees",
                        "Proven robustness in edge cases",
                        "Comprehensive failure mode analysis"
                    ],
                    "weaknesses": [
                        "Limited real-world deployment data",
                        "Computational overhead in safety verification"
                    ]
                })
            else:
                return json.dumps({
                    "scores": {
                        "accuracy": 0.92,
                        "speed": 0.88,
                        "computational_efficiency": 0.85,
                        "sota_comparison": 0.90
                    },
                    "strengths": [
                        "State-of-the-art benchmark performance",
                        "Real-time inference capability",
                        "Scalable architecture"
                    ],
                    "weaknesses": [
                        "Limited safety guarantees",
                        "Performance degradation in rare scenarios"
                    ]
                })
        
        # Synthesis responses
        elif "synthesize" in prompt_lower or "summary" in prompt_lower:
            return json.dumps({
                "summary": "Based on the research analysis, the recommended approach combines robust perception with verified planning algorithms.",
                "key_methods": [
                    "Multi-modal sensor fusion for robust perception",
                    "Model predictive control with safety constraints",
                    "Uncertainty-aware decision making"
                ],
                "deployment_recommendations": [
                    "Implement gradual rollout with extensive testing",
                    "Monitor edge cases and failure modes",
                    "Maintain human oversight for critical scenarios"
                ]
            })
        
        # Default response
        return "Mock LLM response for: " + prompt[:100]


# Global LLM client instance
llm_client = LLMClient(provider="mock")
