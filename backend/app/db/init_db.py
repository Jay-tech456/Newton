"""
Database initialization script.
Creates all tables and seeds initial strategy genomes.
"""
import json
from app.db.database import engine, Base, SessionLocal
from app.models.dataset import Dataset
from app.models.event import Event
from app.models.analysis import Analysis
from app.models.genome import StrategyGenome


def create_initial_genomes(db):
    """Create initial v0.1 genomes for SafetyLab and PerformanceLab"""
    
    safety_genome_v01 = {
        "retrieval_preferences": {
            "year_window": [2018, 2024],
            "venue_weights": {
                "CVPR": 0.9,
                "ICCV": 0.9,
                "NeurIPS": 0.8,
                "ICRA": 1.0,
                "IROS": 1.0,
                "CoRL": 1.0
            },
            "keywords": [
                "autonomous driving safety",
                "collision avoidance",
                "robust perception",
                "safety-critical scenarios",
                "fail-safe planning"
            ],
            "method_categories": [
                "safety_verification",
                "robust_control",
                "uncertainty_estimation"
            ]
        },
        "reading_template": {
            "extract_fields": [
                "method_name",
                "safety_guarantees",
                "failure_modes",
                "robustness_metrics",
                "deployment_notes",
                "limitations"
            ]
        },
        "critique_focus": {
            "dimensions": [
                "robustness",
                "rare_events_handling",
                "safety_metrics",
                "worst_case_performance",
                "failure_recovery"
            ],
            "weights": {
                "robustness": 1.0,
                "rare_events_handling": 1.0,
                "safety_metrics": 1.0,
                "worst_case_performance": 0.9,
                "failure_recovery": 0.8
            }
        },
        "synthesis_style": {
            "audience": "safety_engineers",
            "max_tokens": 600,
            "format": "structured",
            "emphasis": "safety_critical_aspects"
        }
    }
    
    performance_genome_v01 = {
        "retrieval_preferences": {
            "year_window": [2020, 2024],
            "venue_weights": {
                "CVPR": 1.0,
                "ICCV": 1.0,
                "NeurIPS": 1.0,
                "ICML": 0.9,
                "ECCV": 0.9,
                "CoRL": 0.8
            },
            "keywords": [
                "autonomous driving SOTA",
                "real-time perception",
                "efficient planning",
                "end-to-end learning",
                "performance optimization"
            ],
            "method_categories": [
                "deep_learning",
                "reinforcement_learning",
                "imitation_learning",
                "model_based_control"
            ]
        },
        "reading_template": {
            "extract_fields": [
                "method_name",
                "performance_metrics",
                "computational_cost",
                "benchmark_results",
                "deployment_notes",
                "scalability"
            ]
        },
        "critique_focus": {
            "dimensions": [
                "accuracy",
                "speed",
                "computational_efficiency",
                "sota_comparison",
                "scalability"
            ],
            "weights": {
                "accuracy": 1.0,
                "speed": 1.0,
                "computational_efficiency": 0.9,
                "sota_comparison": 0.9,
                "scalability": 0.7
            }
        },
        "synthesis_style": {
            "audience": "ml_engineers",
            "max_tokens": 600,
            "format": "structured",
            "emphasis": "performance_metrics"
        }
    }
    
    # Create SafetyLab genome v0.1
    safety_genome = StrategyGenome(
        lab_name="SafetyLab",
        version="v0.1",
        genome_data=safety_genome_v01,
        parent_version=None,
        change_description="Initial genome for SafetyLab",
        is_active=1
    )
    
    # Create PerformanceLab genome v0.1
    performance_genome = StrategyGenome(
        lab_name="PerformanceLab",
        version="v0.1",
        genome_data=performance_genome_v01,
        parent_version=None,
        change_description="Initial genome for PerformanceLab",
        is_active=1
    )
    
    db.add(safety_genome)
    db.add(performance_genome)
    db.commit()
    
    print("✓ Created initial genomes: SafetyLab v0.1, PerformanceLab v0.1")


def init_db():
    """Initialize database with tables and seed data"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created")
    
    # Create initial genomes
    db = SessionLocal()
    try:
        # Check if genomes already exist
        existing_genomes = db.query(StrategyGenome).count()
        if existing_genomes == 0:
            create_initial_genomes(db)
        else:
            print(f"✓ Database already initialized ({existing_genomes} genomes found)")
    finally:
        db.close()
    
    print("\n✓ Database initialization complete!")


if __name__ == "__main__":
    init_db()
