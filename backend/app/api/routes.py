"""
FastAPI routes for AutoLab Drive.
"""
import os
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from pathlib import Path

from app.db.database import get_db
from app.models.dataset import Dataset
from app.models.event import Event
from app.models.analysis import Analysis
from app.models.genome import StrategyGenome
from app.schemas.dataset import DatasetResponse, DatasetCreate
from app.schemas.event import EventResponse
from app.schemas.analysis import AnalysisResponse
from app.schemas.genome import GenomeResponse, GenomeEvolutionResponse
from app.services.dataset_ingestion import DatasetIngestionService
from app.services.event_detector import EventDetectorService
from app.services.research_lab import ResearchLabOrchestrator
from app.config import settings

router = APIRouter()

# Service instances
dataset_service = DatasetIngestionService()
event_detector = EventDetectorService()
lab_orchestrator = ResearchLabOrchestrator()


@router.post("/api/upload-dataset", response_model=DatasetResponse)
async def upload_dataset(
    file: UploadFile = File(...),
    name: str = Form(...),
    description: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Upload and process a dataset (ZIP file with frames and telemetry.csv).
    """
    # Validate file type
    if not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="Only ZIP files are accepted")
    
    # Save uploaded file temporarily
    temp_path = Path(settings.storage_path) / "temp" / file.filename
    temp_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Ingest dataset
        upload_path, frames_path, telemetry_path, frame_count, duration = \
            dataset_service.ingest_dataset(str(temp_path), name)
        
        # Validate telemetry CSV
        dataset_service.validate_telemetry_csv(telemetry_path)
        
        # Create database record
        dataset = Dataset(
            name=name,
            description=description,
            upload_path=upload_path,
            frames_path=frames_path,
            telemetry_path=telemetry_path,
            frame_count=frame_count,
            duration_seconds=duration
        )
        
        db.add(dataset)
        db.commit()
        db.refresh(dataset)
        
        # Detect events
        telemetry_df = dataset_service.get_telemetry_dataframe(telemetry_path)
        detected_events = event_detector.detect_events(telemetry_df)
        
        # Store events in database
        for event_data in detected_events:
            event = Event(dataset_id=dataset.id, **event_data)
            db.add(event)
        
        db.commit()
        
        return dataset
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process dataset: {str(e)}")
    finally:
        # Clean up temp file
        if temp_path.exists():
            temp_path.unlink()


@router.get("/api/datasets", response_model=List[DatasetResponse])
def list_datasets(db: Session = Depends(get_db)):
    """Get list of all datasets."""
    datasets = db.query(Dataset).order_by(Dataset.created_at.desc()).all()
    return datasets


@router.get("/api/datasets/{dataset_id}", response_model=DatasetResponse)
def get_dataset(dataset_id: int, db: Session = Depends(get_db)):
    """Get dataset by ID."""
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset


@router.delete("/api/datasets/{dataset_id}")
def delete_dataset(dataset_id: int, db: Session = Depends(get_db)):
    """Delete a dataset and all associated data."""
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    try:
        # Delete associated events
        db.query(Event).filter(Event.dataset_id == dataset_id).delete()
        
        # Delete associated analyses
        db.query(Analysis).filter(Analysis.dataset_id == dataset_id).delete()
        
        # Delete dataset files from storage
        if os.path.exists(dataset.upload_path):
            shutil.rmtree(dataset.upload_path)
        
        # Delete database record
        db.delete(dataset)
        db.commit()
        
        return {"message": "Dataset deleted successfully", "id": dataset_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete dataset: {str(e)}")


@router.get("/api/datasets/{dataset_id}/events", response_model=List[EventResponse])
def get_dataset_events(dataset_id: int, db: Session = Depends(get_db)):
    """Get all events for a dataset."""
    # Verify dataset exists
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    events = db.query(Event).filter(Event.dataset_id == dataset_id).order_by(Event.start_timestamp).all()
    return events


@router.post("/api/datasets/{dataset_id}/events/{event_id}/analyze", response_model=AnalysisResponse)
def analyze_event(
    dataset_id: int,
    event_id: int,
    db: Session = Depends(get_db)
):
    """
    Run SafetyLab and PerformanceLab analysis on an event.
    """
    # Get event
    event = db.query(Event).filter(Event.id == event_id, Event.dataset_id == dataset_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Get current active genomes
    safety_genome_record = db.query(StrategyGenome).filter(
        StrategyGenome.lab_name == "SafetyLab",
        StrategyGenome.is_active == 1
    ).order_by(StrategyGenome.created_at.desc()).first()
    
    performance_genome_record = db.query(StrategyGenome).filter(
        StrategyGenome.lab_name == "PerformanceLab",
        StrategyGenome.is_active == 1
    ).order_by(StrategyGenome.created_at.desc()).first()
    
    # If no genomes exist, create default ones
    if not safety_genome_record:
        from app.services.meta_learner import MetaLearner
        meta_learner = MetaLearner()
        _, genome_dict = meta_learner.create_new_genome_version(
            meta_learner.create_initial_genome("SafetyLab"),
            "SafetyLab",
            None,
            "Initial genome for SafetyLab"
        )
        safety_genome_record = StrategyGenome(**genome_dict)
        db.add(safety_genome_record)
        db.commit()
        db.refresh(safety_genome_record)
    
    if not performance_genome_record:
        from app.services.meta_learner import MetaLearner
        meta_learner = MetaLearner()
        _, genome_dict = meta_learner.create_new_genome_version(
            meta_learner.create_initial_genome("PerformanceLab"),
            "PerformanceLab",
            None,
            "Initial genome for PerformanceLab"
        )
        performance_genome_record = StrategyGenome(**genome_dict)
        db.add(performance_genome_record)
        db.commit()
        db.refresh(performance_genome_record)
    
    # Prepare event data
    event_data = {
        "event_type": event.event_type.value,
        "severity": event.severity,
        "ego_speed_mps": event.ego_speed_mps,
        "road_type": event.road_type,
        "weather": event.weather,
        "lead_distance_m": event.lead_distance_m,
        "cut_in_flag": event.cut_in_flag,
        "pedestrian_flag": event.pedestrian_flag
    }
    
    # Run analysis
    analysis_result = lab_orchestrator.run_analysis(
        event_data,
        safety_genome_record.genome_data,
        performance_genome_record.genome_data
    )
    
    # Check if genomes were updated
    new_safety_version = None
    new_performance_version = None
    
    if analysis_result["genome_updates"]["safety_lab"]["updated"]:
        # Create new genome version
        new_version, genome_dict = lab_orchestrator.meta_learner.create_new_genome_version(
            analysis_result["genome_updates"]["safety_lab"]["new_genome"],
            "SafetyLab",
            safety_genome_record.version,
            analysis_result["genome_updates"]["safety_lab"]["changes"]
        )
        new_safety_genome = StrategyGenome(**genome_dict)
        db.add(new_safety_genome)
        new_safety_version = new_version
    
    if analysis_result["genome_updates"]["performance_lab"]["updated"]:
        # Create new genome version
        new_version, genome_dict = lab_orchestrator.meta_learner.create_new_genome_version(
            analysis_result["genome_updates"]["performance_lab"]["new_genome"],
            "PerformanceLab",
            performance_genome_record.version,
            analysis_result["genome_updates"]["performance_lab"]["changes"]
        )
        new_performance_genome = StrategyGenome(**genome_dict)
        db.add(new_performance_genome)
        new_performance_version = new_version
    
    # Create analysis record
    analysis = Analysis(
        event_id=event_id,
        safety_lab_output=analysis_result["safety_lab_output"],
        performance_lab_output=analysis_result["performance_lab_output"],
        judge_decision=analysis_result["judge_decision"],
        safety_genome_version=safety_genome_record.version,
        performance_genome_version=performance_genome_record.version,
        new_safety_genome_version=new_safety_version,
        new_performance_genome_version=new_performance_version,
        duration_seconds=int(analysis_result["total_duration_seconds"])
    )
    
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    
    return analysis


@router.get("/api/datasets/{dataset_id}/events/{event_id}/analysis", response_model=AnalysisResponse)
def get_event_analysis(
    dataset_id: int,
    event_id: int,
    db: Session = Depends(get_db)
):
    """Get cached analysis for an event."""
    # Verify event exists
    event = db.query(Event).filter(Event.id == event_id, Event.dataset_id == dataset_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Get most recent analysis
    analysis = db.query(Analysis).filter(Analysis.event_id == event_id).order_by(Analysis.created_at.desc()).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="No analysis found for this event")
    
    return analysis


@router.get("/api/labs/strategies", response_model=List[GenomeEvolutionResponse])
def get_lab_strategies(db: Session = Depends(get_db)):
    """Get genome evolution for all labs."""
    results = []
    
    for lab_name in ["SafetyLab", "PerformanceLab"]:
        genomes = db.query(StrategyGenome).filter(
            StrategyGenome.lab_name == lab_name
        ).order_by(StrategyGenome.created_at).all()
        
        results.append({
            "lab_name": lab_name,
            "versions": genomes
        })
    
    return results


@router.get("/api/labs/{lab_name}/strategies", response_model=GenomeEvolutionResponse)
def get_lab_strategy_evolution(lab_name: str, db: Session = Depends(get_db)):
    """Get genome evolution for a specific lab."""
    if lab_name not in ["SafetyLab", "PerformanceLab"]:
        raise HTTPException(status_code=400, detail="Invalid lab name")
    
    genomes = db.query(StrategyGenome).filter(
        StrategyGenome.lab_name == lab_name
    ).order_by(StrategyGenome.created_at).all()
    
    return {
        "lab_name": lab_name,
        "versions": genomes
    }


@router.get("/api/datasets/{dataset_id}/frames/{frame_number}")
def get_frame(dataset_id: int, frame_number: int, db: Session = Depends(get_db)):
    """Serve a specific frame from a dataset."""
    # Get dataset
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Construct frame path
    frame_filename = f"frame_{frame_number:06d}.jpg"
    frame_path = Path(dataset.frames_path) / frame_filename
    
    if not frame_path.exists():
        raise HTTPException(status_code=404, detail="Frame not found")
    
    return FileResponse(frame_path, media_type="image/jpeg")


@router.get("/api/health")
def health_check():
    """Health check endpoint for Docker."""
    return {"status": "healthy"}
