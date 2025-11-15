# AutoLab Drive - Architecture Documentation

## System Overview

AutoLab Drive is a self-evolving multi-agent research system for autonomous driving that:
1. Ingests real driving datasets
2. Detects scenario events
3. Runs competing research labs (SafetyLab & PerformanceLab)
4. Compares outputs via Judge agent
5. Evolves lab strategies via Meta-Learner

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend (React)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Datasets   │  │    Events    │  │  Strategies  │      │
│  │     Page     │  │   Timeline   │  │   Evolution  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │ HTTP/REST
┌─────────────────────────────────────────────────────────────┐
│                      Backend (FastAPI)                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                    API Endpoints                      │   │
│  │  /upload-dataset  /events  /analyze  /strategies     │   │
│  └──────────────────────────────────────────────────────┘   │
│                            │                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                 Service Layer                         │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐     │   │
│  │  │  Dataset   │  │   Event    │  │  Research  │     │   │
│  │  │ Ingestion  │  │  Detector  │  │    Lab     │     │   │
│  │  └────────────┘  └────────────┘  └────────────┘     │   │
│  └──────────────────────────────────────────────────────┘   │
│                            │                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Multi-Agent System                       │   │
│  │  ┌─────────────────────────────────────────────┐     │   │
│  │  │            SafetyLab                        │     │   │
│  │  │  Planner → Retriever → Reader → Critic →   │     │   │
│  │  │                    Synthesizer              │     │   │
│  │  └─────────────────────────────────────────────┘     │   │
│  │  ┌─────────────────────────────────────────────┐     │   │
│  │  │         PerformanceLab                      │     │   │
│  │  │  Planner → Retriever → Reader → Critic →   │     │   │
│  │  │                    Synthesizer              │     │   │
│  │  └─────────────────────────────────────────────┘     │   │
│  │                     │         │                       │   │
│  │              ┌──────┴─────────┴──────┐               │   │
│  │              │       Judge           │               │   │
│  │              └───────────┬───────────┘               │   │
│  │                          │                           │   │
│  │              ┌───────────▼───────────┐               │   │
│  │              │    Meta-Learner       │               │   │
│  │              │  (Genome Evolution)   │               │   │
│  │              └───────────────────────┘               │   │
│  └──────────────────────────────────────────────────────┘   │
│                            │                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                  Data Layer                           │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐           │   │
│  │  │ Datasets │  │  Events  │  │ Genomes  │           │   │
│  │  └──────────┘  └──────────┘  └──────────┘           │   │
│  │  SQLite/PostgreSQL + File Storage                    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Dataset Ingestion Pipeline

**Input:** ZIP file containing frames/ and telemetry.csv

**Process:**
1. Extract ZIP to storage directory
2. Validate telemetry CSV structure
3. Count frames and calculate duration
4. Store metadata in database
5. Trigger event detection

**Key Files:**
- `backend/app/services/dataset_ingestion.py`
- `backend/app/models/dataset.py`

### 2. Event Detection

**Input:** Telemetry DataFrame

**Detection Rules:**
- **Cut-in:** `cut_in_flag == 1`
- **Pedestrian:** `pedestrian_flag == 1`
- **Adverse Weather:** `weather != 'clear'`
- **Close Following:** `lead_distance_m < 15.0`
- **Sudden Brake:** Speed drop > 5 m/s in 1 second
- **Lane Change:** Yaw change > 10° in 2 seconds

**Output:** List of Event objects with metadata

**Key Files:**
- `backend/app/services/event_detector.py`
- `backend/app/models/event.py`

### 3. Multi-Agent Research System

#### Agent Pipeline

Each lab (SafetyLab & PerformanceLab) runs the same pipeline with different genomes:

```
Event → Planner → Retriever → Reader → Critic → Synthesizer → Output
```

**Agent Responsibilities:**

1. **Planner** (`planner.py`)
   - Generates research questions based on event and genome
   - Extracts keywords and priority dimensions
   - Creates search strategy

2. **Retriever** (`retriever.py`)
   - Retrieves relevant papers (currently mock data)
   - Filters by year window and venue weights
   - Returns top N papers

3. **Reader** (`reader.py`)
   - Extracts structured information from papers
   - Uses genome's reading template
   - Populates fields like safety_guarantees, performance_metrics, etc.

4. **Critic** (`critic.py`)
   - Evaluates papers on genome-specific dimensions
   - Calculates weighted scores
   - Identifies strengths and weaknesses

5. **Synthesizer** (`synthesizer.py`)
   - Combines findings into actionable recommendations
   - Formats output for target audience
   - Provides confidence level

#### Judge Agent

**Input:** SafetyLab output + PerformanceLab output + Event context

**Process:**
1. Compare outputs on multiple dimensions
2. Calculate scores for each lab
3. Determine winner (or tie)
4. Provide detailed reasoning
5. Generate improvement recommendations

**Output:** JudgeDecision with scores and feedback

**Key File:** `backend/app/agents/judge.py`

#### Meta-Learner Agent

**Input:** Judge decision + Current genomes + Event context

**Process:**
1. Analyze judge feedback
2. Update losing lab's genome:
   - Adopt keywords from winner
   - Adjust critique dimension weights
   - Update year window if needed
3. Reinforce winning lab's successful strategies
4. Create new genome versions

**Output:** Updated genomes (if changes made)

**Key File:** `backend/app/agents/meta_learner.py`

### 4. Strategy Genome

Each lab maintains a genome that defines its research strategy:

```json
{
  "retrieval_preferences": {
    "year_window": [2018, 2024],
    "venue_weights": {
      "CVPR": 1.0,
      "ICCV": 0.9,
      "NeurIPS": 0.8
    },
    "keywords": [
      "autonomous driving safety",
      "collision avoidance"
    ]
  },
  "reading_template": {
    "extract_fields": [
      "method_name",
      "safety_guarantees",
      "robustness_metrics"
    ]
  },
  "critique_focus": {
    "dimensions": [
      "robustness",
      "rare_events_handling",
      "safety_metrics"
    ],
    "weights": {
      "robustness": 1.0,
      "rare_events_handling": 0.9
    }
  },
  "synthesis_style": {
    "audience": "safety_engineers",
    "max_tokens": 600,
    "emphasis": "safety_critical_aspects"
  }
}
```

**Evolution Mechanism:**
- Genomes are versioned (v0.1, v0.2, etc.)
- Each version has a parent_version and change_description
- Active genome is used for new analyses
- Historical genomes are preserved for tracking

**Key File:** `backend/app/models/genome.py`

### 5. Database Schema

**Tables:**

1. **datasets**
   - id, name, description, paths, frame_count, duration, created_at

2. **events**
   - id, dataset_id, event_type, timestamps, context, severity, created_at

3. **analyses**
   - id, event_id, lab_outputs (JSON), judge_decision (JSON), genome_versions, created_at

4. **strategy_genomes**
   - id, lab_name, version, genome_data (JSON), parent_version, change_description, is_active, created_at

**Key File:** `backend/app/db/database.py`

### 6. Frontend Architecture

**Tech Stack:**
- React 18 + TypeScript
- Vite (build tool)
- TailwindCSS (styling)
- React Router (navigation)
- Axios (API client)
- Lucide React (icons)

**Pages:**

1. **DatasetsPage** (`/`)
   - List all datasets
   - Upload modal
   - Dataset cards with metadata

2. **DatasetDetailPage** (`/datasets/:id`)
   - Event timeline visualization
   - Event details panel
   - Analysis panel (SafetyLab vs PerformanceLab)
   - Judge decision display

3. **StrategiesPage** (`/strategies`)
   - Lab selector (SafetyLab / PerformanceLab)
   - Genome evolution timeline
   - Expandable version cards with details

**Key Components:**
- `Layout.tsx`: Header, navigation, footer
- `EventTimeline.tsx`: Visual timeline with event markers
- `AnalysisPanel.tsx`: Side-by-side lab comparison

## Data Flow

### Upload Dataset Flow

```
User uploads ZIP
    ↓
Frontend: POST /api/upload-dataset
    ↓
Backend: DatasetIngestionService
    ↓
Extract ZIP, validate CSV
    ↓
Store in database
    ↓
EventDetectorService
    ↓
Detect events from telemetry
    ↓
Store events in database
    ↓
Return dataset with event count
```

### Analysis Flow

```
User clicks "Run Analysis"
    ↓
Frontend: POST /api/datasets/{id}/events/{event_id}/analyze
    ↓
Backend: ResearchLabOrchestrator
    ↓
Get active genomes from database
    ↓
┌─────────────────┬─────────────────┐
│   SafetyLab     │ PerformanceLab  │
│   (parallel)    │   (parallel)    │
└─────────────────┴─────────────────┘
    ↓           ↓
    └───────┬───────┘
            ↓
        Judge Agent
            ↓
    Meta-Learner Agent
            ↓
    Update genomes (if needed)
            ↓
    Store analysis in database
            ↓
    Return complete analysis
```

## Extension Points

### 1. Replace Mock LLM

**Current:** `app/agents/llm_client.py` returns hardcoded responses

**To integrate real LLM:**
```python
class LLMClient:
    def __init__(self, provider: str = "openai"):
        if provider == "openai":
            import openai
            self.client = openai.OpenAI(api_key=settings.llm_api_key)
    
    def generate(self, prompt: str, context: Dict = None) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
```

### 2. Connect Research APIs

**Current:** `app/agents/retriever.py` returns mock papers

**To integrate arXiv:**
```python
import arxiv

def retrieve_from_arxiv(keywords: List[str], max_results: int = 10):
    search = arxiv.Search(
        query=" ".join(keywords),
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )
    
    papers = []
    for result in search.results():
        papers.append({
            "title": result.title,
            "authors": [a.name for a in result.authors],
            "abstract": result.summary,
            "year": result.published.year,
            # ... more fields
        })
    return papers
```

### 3. Add Real-Time Streaming

**Current:** Batch processing of uploaded datasets

**To add streaming:**
- WebSocket endpoint for real-time telemetry
- Streaming event detection
- Live analysis updates
- Real-time genome evolution

### 4. Multi-Modal Analysis

**Current:** CSV telemetry only

**To add vision:**
- Frame analysis with computer vision models
- Object detection integration
- Scene understanding
- Visual failure mode detection

## Performance Considerations

### Current Limitations

1. **Sequential Analysis:** Labs run in parallel, but agents within each lab are sequential
2. **In-Memory Processing:** All data loaded into memory
3. **No Caching:** Papers retrieved fresh each time
4. **Synchronous API:** Blocking requests during analysis

### Optimization Strategies

1. **Async Processing:**
   - Use Celery for background tasks
   - Queue analysis jobs
   - WebSocket for progress updates

2. **Caching:**
   - Redis for paper cache
   - Memoize LLM responses
   - Cache genome computations

3. **Parallel Agents:**
   - Run Planner, Retriever, Reader in parallel
   - Batch LLM requests
   - Concurrent paper processing

4. **Database Optimization:**
   - Index frequently queried fields
   - Use PostgreSQL for production
   - Implement connection pooling

## Security Considerations

1. **File Upload:**
   - Validate ZIP contents
   - Scan for malicious files
   - Limit file sizes
   - Sanitize filenames

2. **API Security:**
   - Add authentication (JWT)
   - Rate limiting
   - Input validation
   - CORS configuration

3. **Data Privacy:**
   - Encrypt sensitive data
   - Secure file storage
   - Access control
   - Audit logging

## Testing Strategy

### Unit Tests
- Agent logic
- Event detection rules
- Genome evolution
- API endpoints

### Integration Tests
- Full analysis pipeline
- Database operations
- File upload/processing

### End-to-End Tests
- Frontend workflows
- API integration
- Multi-agent coordination

## Deployment

### Development
```bash
# Backend
cd backend && uvicorn app.main:app --reload

# Frontend
cd frontend && npm run dev
```

### Production
```bash
# Backend
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Frontend
npm run build
# Serve dist/ with nginx or CDN
```

### Docker
```dockerfile
# Backend Dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]

# Frontend Dockerfile
FROM node:18 as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
```

## Monitoring & Observability

### Metrics to Track
- Analysis duration per event
- Genome evolution frequency
- Judge decision distribution
- API response times
- Error rates

### Logging
- Structured logging with JSON
- Log levels (DEBUG, INFO, WARNING, ERROR)
- Request/response logging
- Agent decision logging

### Alerting
- Failed analyses
- Database errors
- API downtime
- Unusual genome mutations

## Future Enhancements

1. **Advanced Evolution:**
   - Genetic algorithms for genome optimization
   - Multi-objective optimization
   - A/B testing of strategies

2. **Collaborative Labs:**
   - More than 2 labs
   - Specialized labs (e.g., PerceptionLab, PlanningLab)
   - Lab cooperation mechanisms

3. **Human-in-the-Loop:**
   - Manual genome editing
   - Expert feedback integration
   - Annotation tools

4. **Explainability:**
   - Visualize agent reasoning
   - Decision trees
   - Attention mechanisms
   - Counterfactual analysis
