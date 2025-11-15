"""
Research Lab Orchestrator
Coordinates multi-agent workflow for SafetyLab and PerformanceLab.
"""
import time
from typing import Dict, Any
from app.agents.planner import PlannerAgent
from app.agents.retriever import RetrieverAgent
from app.agents.reader import ReaderAgent
from app.agents.critic import CriticAgent
from app.agents.synthesizer import SynthesizerAgent
from app.agents.judge import JudgeAgent
from app.agents.meta_learner import MetaLearnerAgent


class ResearchLab:
    """
    Orchestrates the multi-agent research workflow for a single lab.
    """
    
    def __init__(self, lab_name: str, genome: Dict[str, Any]):
        self.lab_name = lab_name
        self.genome = genome
        
        # Initialize agents
        self.planner = PlannerAgent(lab_name, genome)
        self.retriever = RetrieverAgent(lab_name, genome)
        self.reader = ReaderAgent(lab_name, genome)
        self.critic = CriticAgent(lab_name, genome)
        self.synthesizer = SynthesizerAgent(lab_name, genome)
    
    def analyze_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run complete research workflow for an event.
        
        Args:
            event_data: Event metadata
            
        Returns:
            Lab output with synthesis and intermediate results
        """
        start_time = time.time()
        
        # Step 1: Planning
        research_plan = self.planner.plan(event_data)
        
        # Step 2: Retrieval
        papers = self.retriever.retrieve(research_plan)
        
        # Step 3: Reading
        extracted_papers = self.reader.read(papers)
        
        # Step 4: Critique
        critiqued_papers = self.critic.critique(extracted_papers, event_data)
        
        # Step 5: Synthesis
        synthesis = self.synthesizer.synthesize(research_plan, critiqued_papers, event_data)
        
        duration = time.time() - start_time
        
        return {
            "lab_name": self.lab_name,
            "research_plan": research_plan,
            "papers_analyzed": len(papers),
            "top_papers": critiqued_papers[:5],
            "synthesis": synthesis,
            "duration_seconds": round(duration, 2)
        }


class ResearchLabOrchestrator:
    """
    Orchestrates both SafetyLab and PerformanceLab, plus Judge and Meta-Learner.
    """
    
    def __init__(self):
        self.judge = JudgeAgent()
        self.meta_learner = MetaLearnerAgent()
    
    def run_analysis(
        self,
        event_data: Dict[str, Any],
        safety_genome: Dict[str, Any],
        performance_genome: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Run complete analysis with both labs, judge, and meta-learner.
        
        Args:
            event_data: Event metadata
            safety_genome: SafetyLab genome
            performance_genome: PerformanceLab genome
            
        Returns:
            Complete analysis results
        """
        start_time = time.time()
        
        # Initialize labs
        safety_lab = ResearchLab("SafetyLab", safety_genome)
        performance_lab = ResearchLab("PerformanceLab", performance_genome)
        
        # Run both labs
        safety_output = safety_lab.analyze_event(event_data)
        performance_output = performance_lab.analyze_event(event_data)
        
        # Judge comparison
        judge_decision = self.judge.judge(
            safety_output["synthesis"],
            performance_output["synthesis"],
            event_data
        )
        
        # Meta-learner updates genomes
        (
            new_safety_genome,
            new_performance_genome,
            safety_changes,
            performance_changes
        ) = self.meta_learner.learn(
            judge_decision,
            safety_genome,
            performance_genome,
            event_data
        )
        
        total_duration = time.time() - start_time
        
        return {
            "safety_lab_output": safety_output,
            "performance_lab_output": performance_output,
            "judge_decision": judge_decision,
            "genome_updates": {
                "safety_lab": {
                    "updated": safety_changes != "No changes",
                    "changes": safety_changes,
                    "new_genome": new_safety_genome
                },
                "performance_lab": {
                    "updated": performance_changes != "No changes",
                    "changes": performance_changes,
                    "new_genome": new_performance_genome
                }
            },
            "total_duration_seconds": round(total_duration, 2)
        }
