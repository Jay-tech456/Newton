"""
Google DeepMind Integration
Method categorization based on DeepMind-style RL/control paradigms.
"""
from enum import Enum
from typing import List, Dict, Any


class MethodCategory(str, Enum):
    """
    Method categories inspired by Google DeepMind research taxonomy.
    """
    # Reinforcement Learning
    RL_MODEL_FREE = "rl_model_free"
    RL_MODEL_BASED = "rl_model_based"
    RL_OFFLINE = "rl_offline"
    RL_SAFE = "rl_safe"
    
    # Imitation Learning
    IMITATION_BEHAVIORAL_CLONING = "imitation_behavioral_cloning"
    IMITATION_INVERSE_RL = "imitation_inverse_rl"
    IMITATION_GAIL = "imitation_gail"
    
    # Control
    CONTROL_MODEL_PREDICTIVE = "control_model_predictive"
    CONTROL_OPTIMAL = "control_optimal"
    CONTROL_ROBUST = "control_robust"
    
    # Perception
    PERCEPTION_DEEP_LEARNING = "perception_deep_learning"
    PERCEPTION_MULTI_MODAL = "perception_multi_modal"
    PERCEPTION_3D = "perception_3d"
    
    # End-to-End
    END_TO_END_LEARNING = "end_to_end_learning"
    END_TO_END_DIFFERENTIABLE = "end_to_end_differentiable"
    
    # Verification & Safety
    SAFETY_VERIFICATION = "safety_verification"
    SAFETY_SHIELDING = "safety_shielding"
    UNCERTAINTY_ESTIMATION = "uncertainty_estimation"
    
    # Other
    OTHER = "other"


class DeepMindCategorizer:
    """
    Categorizes autonomous driving methods using DeepMind-inspired taxonomy.
    """
    
    @staticmethod
    def categorize_method(method_description: str, paper_title: str = "") -> MethodCategory:
        """
        Categorize a method based on description and title.
        
        Args:
            method_description: Method description or abstract
            paper_title: Paper title
            
        Returns:
            MethodCategory enum
        """
        text = (method_description + " " + paper_title).lower()
        
        # RL categories
        if "reinforcement learning" in text or "rl" in text:
            if "model-based" in text or "world model" in text:
                return MethodCategory.RL_MODEL_BASED
            elif "offline" in text or "batch" in text:
                return MethodCategory.RL_OFFLINE
            elif "safe" in text or "constrained" in text:
                return MethodCategory.RL_SAFE
            else:
                return MethodCategory.RL_MODEL_FREE
        
        # Imitation learning
        if "imitation" in text or "demonstration" in text:
            if "inverse" in text:
                return MethodCategory.IMITATION_INVERSE_RL
            elif "gail" in text or "adversarial" in text:
                return MethodCategory.IMITATION_GAIL
            else:
                return MethodCategory.IMITATION_BEHAVIORAL_CLONING
        
        # Control
        if "mpc" in text or "model predictive" in text:
            return MethodCategory.CONTROL_MODEL_PREDICTIVE
        if "optimal control" in text or "lqr" in text:
            return MethodCategory.CONTROL_OPTIMAL
        if "robust control" in text or "h-infinity" in text:
            return MethodCategory.CONTROL_ROBUST
        
        # Perception
        if "perception" in text or "detection" in text or "segmentation" in text:
            if "multi-modal" in text or "fusion" in text:
                return MethodCategory.PERCEPTION_MULTI_MODAL
            elif "3d" in text or "point cloud" in text:
                return MethodCategory.PERCEPTION_3D
            else:
                return MethodCategory.PERCEPTION_DEEP_LEARNING
        
        # End-to-end
        if "end-to-end" in text or "e2e" in text:
            if "differentiable" in text:
                return MethodCategory.END_TO_END_DIFFERENTIABLE
            else:
                return MethodCategory.END_TO_END_LEARNING
        
        # Safety & verification
        if "verification" in text or "formal methods" in text:
            return MethodCategory.SAFETY_VERIFICATION
        if "shield" in text or "safety layer" in text:
            return MethodCategory.SAFETY_SHIELDING
        if "uncertainty" in text or "bayesian" in text:
            return MethodCategory.UNCERTAINTY_ESTIMATION
        
        return MethodCategory.OTHER
    
    @staticmethod
    def get_category_description(category: MethodCategory) -> str:
        """Get human-readable description of category."""
        descriptions = {
            MethodCategory.RL_MODEL_FREE: "Model-free reinforcement learning (e.g., DQN, PPO, SAC)",
            MethodCategory.RL_MODEL_BASED: "Model-based RL with learned world models",
            MethodCategory.RL_OFFLINE: "Offline/batch RL from logged data",
            MethodCategory.RL_SAFE: "Safe RL with constraints and guarantees",
            MethodCategory.IMITATION_BEHAVIORAL_CLONING: "Behavioral cloning from expert demonstrations",
            MethodCategory.IMITATION_INVERSE_RL: "Inverse RL to learn reward functions",
            MethodCategory.IMITATION_GAIL: "Generative adversarial imitation learning",
            MethodCategory.CONTROL_MODEL_PREDICTIVE: "Model predictive control (MPC)",
            MethodCategory.CONTROL_OPTIMAL: "Optimal control (LQR, LQG, etc.)",
            MethodCategory.CONTROL_ROBUST: "Robust control for uncertainty",
            MethodCategory.PERCEPTION_DEEP_LEARNING: "Deep learning for perception",
            MethodCategory.PERCEPTION_MULTI_MODAL: "Multi-modal sensor fusion",
            MethodCategory.PERCEPTION_3D: "3D object detection and tracking",
            MethodCategory.END_TO_END_LEARNING: "End-to-end learning from sensors to actions",
            MethodCategory.END_TO_END_DIFFERENTIABLE: "Fully differentiable driving pipelines",
            MethodCategory.SAFETY_VERIFICATION: "Formal safety verification",
            MethodCategory.SAFETY_SHIELDING: "Safety shielding and intervention",
            MethodCategory.UNCERTAINTY_ESTIMATION: "Uncertainty quantification",
            MethodCategory.OTHER: "Other methods"
        }
        return descriptions.get(category, "Unknown category")
    
    @staticmethod
    def get_category_strengths_weaknesses(category: MethodCategory) -> Dict[str, List[str]]:
        """Get typical strengths and weaknesses for each category."""
        profiles = {
            MethodCategory.RL_MODEL_FREE: {
                "strengths": ["Can learn complex behaviors", "No model required", "Proven in many domains"],
                "weaknesses": ["Sample inefficient", "Limited safety guarantees", "Difficult to interpret"]
            },
            MethodCategory.RL_MODEL_BASED: {
                "strengths": ["Sample efficient", "Can plan ahead", "Interpretable world model"],
                "weaknesses": ["Model errors compound", "Computational overhead", "Difficult to learn accurate models"]
            },
            MethodCategory.CONTROL_MODEL_PREDICTIVE: {
                "strengths": ["Explicit constraints", "Predictable behavior", "Well-understood theory"],
                "weaknesses": ["Requires accurate model", "Computational cost", "Limited to model accuracy"]
            },
            MethodCategory.SAFETY_VERIFICATION: {
                "strengths": ["Formal guarantees", "Provable safety", "Comprehensive analysis"],
                "weaknesses": ["Computational complexity", "Conservative behavior", "Limited scalability"]
            },
            MethodCategory.END_TO_END_LEARNING: {
                "strengths": ["Learns from raw data", "No manual feature engineering", "Can discover novel strategies"],
                "weaknesses": ["Black box", "Requires large datasets", "Limited interpretability"]
            }
        }
        return profiles.get(category, {
            "strengths": ["Method-specific strengths"],
            "weaknesses": ["Method-specific weaknesses"]
        })


# Global categorizer instance
deepmind_categorizer = DeepMindCategorizer()
