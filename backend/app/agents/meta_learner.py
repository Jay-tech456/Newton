"""
Meta-Learner Agent
Updates strategy genomes based on Judge feedback.
"""
import copy
from typing import Dict, Any, Tuple
from datetime import datetime


class MetaLearnerAgent:
    """
    Evolves lab genomes based on performance feedback.
    Implements simple learning rules that can be extended.
    """
    
    def learn(
        self,
        judge_decision: Dict[str, Any],
        safety_genome: Dict[str, Any],
        performance_genome: Dict[str, Any],
        event_data: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], Dict[str, Any], str, str]:
        """
        Update genomes based on judge feedback.
        
        Args:
            judge_decision: Judge's evaluation
            safety_genome: Current SafetyLab genome
            performance_genome: Current PerformanceLab genome
            event_data: Event context
            
        Returns:
            Tuple of (new_safety_genome, new_performance_genome, safety_changes, performance_changes)
        """
        winner = judge_decision.get("winner", "Tie")
        safety_score = judge_decision.get("safety_lab_score", 0.75)
        performance_score = judge_decision.get("performance_lab_score", 0.75)
        recommendations = judge_decision.get("recommendations_for_improvement", {})
        
        # Deep copy genomes for modification
        new_safety_genome = copy.deepcopy(safety_genome)
        new_performance_genome = copy.deepcopy(performance_genome)
        
        safety_changes = []
        performance_changes = []
        
        # Update SafetyLab genome
        if winner == "PerformanceLab" or safety_score < 0.7:
            # SafetyLab needs improvement
            safety_changes = self._update_losing_genome(
                new_safety_genome,
                performance_genome,
                recommendations.get("SafetyLab", []),
                "SafetyLab"
            )
        elif winner == "SafetyLab":
            # SafetyLab won - reinforce successful strategies
            safety_changes = self._reinforce_winning_genome(
                new_safety_genome,
                "SafetyLab"
            )
        
        # Update PerformanceLab genome
        if winner == "SafetyLab" or performance_score < 0.7:
            # PerformanceLab needs improvement
            performance_changes = self._update_losing_genome(
                new_performance_genome,
                safety_genome,
                recommendations.get("PerformanceLab", []),
                "PerformanceLab"
            )
        elif winner == "PerformanceLab":
            # PerformanceLab won - reinforce successful strategies
            performance_changes = self._reinforce_winning_genome(
                new_performance_genome,
                "PerformanceLab"
            )
        
        # If tie, make minor adjustments to both
        if winner == "Tie":
            safety_changes = self._minor_adjustments(new_safety_genome, "SafetyLab")
            performance_changes = self._minor_adjustments(new_performance_genome, "PerformanceLab")
        
        return (
            new_safety_genome,
            new_performance_genome,
            "; ".join(safety_changes) if safety_changes else "No changes",
            "; ".join(performance_changes) if performance_changes else "No changes"
        )
    
    def _update_losing_genome(
        self,
        genome: Dict[str, Any],
        winning_genome: Dict[str, Any],
        recommendations: list,
        lab_name: str
    ) -> list:
        """Update genome for losing lab"""
        changes = []
        
        # 1. Adopt some keywords from winning lab
        winning_keywords = winning_genome.get("retrieval_preferences", {}).get("keywords", [])
        current_keywords = genome.get("retrieval_preferences", {}).get("keywords", [])
        
        # Add 1-2 keywords from winner if not already present
        new_keywords = [kw for kw in winning_keywords if kw not in current_keywords][:2]
        if new_keywords:
            genome["retrieval_preferences"]["keywords"].extend(new_keywords)
            changes.append(f"Added keywords: {', '.join(new_keywords)}")
        
        # 2. Adjust critique dimension weights
        critique_focus = genome.get("critique_focus", {})
        weights = critique_focus.get("weights", {})
        
        # Slightly increase weights for dimensions mentioned in recommendations
        for rec in recommendations:
            rec_lower = rec.lower()
            for dimension in weights.keys():
                if dimension.replace("_", " ") in rec_lower:
                    old_weight = weights[dimension]
                    weights[dimension] = min(old_weight + 0.1, 1.0)
                    changes.append(f"Increased weight for '{dimension}' from {old_weight:.2f} to {weights[dimension]:.2f}")
        
        # 3. Adjust year window to be more recent if recommendations mention "latest" or "recent"
        if any("latest" in rec.lower() or "recent" in rec.lower() for rec in recommendations):
            year_window = genome.get("retrieval_preferences", {}).get("year_window", [2018, 2024])
            if year_window[0] < 2020:
                genome["retrieval_preferences"]["year_window"][0] = 2020
                changes.append("Updated year window to focus on more recent research (2020-2024)")
        
        return changes if changes else ["Minor parameter adjustments"]
    
    def _reinforce_winning_genome(self, genome: Dict[str, Any], lab_name: str) -> list:
        """Reinforce successful strategies in winning genome"""
        changes = []
        
        # Slightly increase weights for top-performing dimensions
        critique_focus = genome.get("critique_focus", {})
        weights = critique_focus.get("weights", {})
        
        # Find highest weighted dimension and increase it slightly
        if weights:
            max_dim = max(weights, key=weights.get)
            old_weight = weights[max_dim]
            weights[max_dim] = min(old_weight + 0.05, 1.0)
            changes.append(f"Reinforced '{max_dim}' weight from {old_weight:.2f} to {weights[max_dim]:.2f}")
        
        return changes if changes else ["Maintained successful strategy"]
    
    def _minor_adjustments(self, genome: Dict[str, Any], lab_name: str) -> list:
        """Make minor adjustments for tie scenario"""
        changes = []
        
        # Slightly adjust venue weights
        venue_weights = genome.get("retrieval_preferences", {}).get("venue_weights", {})
        if venue_weights:
            # Increase weight for top venue
            max_venue = max(venue_weights, key=venue_weights.get)
            old_weight = venue_weights[max_venue]
            venue_weights[max_venue] = min(old_weight + 0.05, 1.0)
            changes.append(f"Increased {max_venue} weight from {old_weight:.2f} to {venue_weights[max_venue]:.2f}")
        
        return changes if changes else ["No significant changes"]
    
    def create_initial_genome(self, lab_name: str) -> Dict[str, Any]:
        """
        Create initial genome for a lab.
        
        Args:
            lab_name: Name of the lab (SafetyLab or PerformanceLab)
            
        Returns:
            Initial genome configuration
        """
        if lab_name == "SafetyLab":
            return {
                "retrieval_preferences": {
                    "keywords": [
                        "collision avoidance",
                        "safety critical systems",
                        "risk assessment",
                        "autonomous driving safety",
                        "pedestrian detection"
                    ],
                    "venue_weights": {
                        "ICRA": 0.9,
                        "IV": 0.85,
                        "IROS": 0.8,
                        "ITSC": 0.75
                    },
                    "year_window": [2018, 2024]
                },
                "critique_focus": {
                    "weights": {
                        "safety": 0.9,
                        "robustness": 0.8,
                        "novelty": 0.6,
                        "computational_efficiency": 0.3
                    }
                }
            }
        else:  # PerformanceLab
            return {
                "retrieval_preferences": {
                    "keywords": [
                        "optimization",
                        "computational efficiency",
                        "real-time processing",
                        "neural network acceleration",
                        "model compression"
                    ],
                    "venue_weights": {
                        "CVPR": 0.9,
                        "NeurIPS": 0.85,
                        "ICCV": 0.8,
                        "ECCV": 0.75
                    },
                    "year_window": [2020, 2024]
                },
                "critique_focus": {
                    "weights": {
                        "computational_efficiency": 0.9,
                        "novelty": 0.8,
                        "robustness": 0.6,
                        "safety": 0.3
                    }
                }
            }
    
    def create_new_genome_version(
        self,
        genome_data: Dict[str, Any],
        lab_name: str,
        current_version: str,
        change_description: str
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Create new genome version.
        
        Returns:
            Tuple of (new_version, genome_dict_for_db)
        """
        # Parse current version (e.g., "v0.1" -> 0.1)
        if current_version is None:
            new_version = "v0.1"
        else:
            try:
                version_num = float(current_version.replace("v", ""))
                new_version_num = round(version_num + 0.1, 1)
                new_version = f"v{new_version_num}"
            except:
                new_version = "v0.2"
        
        genome_dict = {
            "lab_name": lab_name,
            "version": new_version,
            "genome_data": genome_data,
            "parent_version": current_version,
            "change_description": change_description,
            "is_active": 1
        }
        
        return new_version, genome_dict
