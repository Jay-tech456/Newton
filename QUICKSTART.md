# AutoLab Drive - Quick Start Guide

## Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **npm or yarn**

## Setup Instructions

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp ../.env.example .env

# Initialize database and create initial genomes
python -m app.db.init_db

# Run the backend server
uvicorn app.main:app --reload --port 8000
```

The backend API will be available at `http://localhost:8000`
- API docs: `http://localhost:8000/docs`

### 2. Frontend Setup

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Usage

### 1. Upload a Dataset

1. Navigate to `http://localhost:5173`
2. Click "Upload Dataset"
3. Provide:
   - Dataset name
   - Optional description
   - ZIP file containing:
     - `frames/` directory with images (frame_000001.jpg, frame_000002.jpg, etc.)
     - `telemetry.csv` with required columns

### 2. Analyze Events

1. Click on a dataset to view details
2. Browse detected events on the timeline
3. Select an event to view details
4. Click "Run Analysis" to start multi-agent research
5. View SafetyLab vs PerformanceLab outputs
6. See Judge decision and genome evolution

### 3. Track Strategy Evolution

1. Navigate to "Lab Strategies" page
2. Switch between SafetyLab and PerformanceLab
3. View genome evolution timeline
4. Expand versions to see detailed changes

## Sample Dataset Format

### Directory Structure
```
dataset.zip
├── frames/
│   ├── frame_000001.jpg
│   ├── frame_000002.jpg
│   └── ...
└── telemetry.csv
```

### telemetry.csv Format
```csv
frame_id,timestamp,ego_speed_mps,ego_yaw,road_type,weather,lead_distance_m,cut_in_flag,pedestrian_flag
frame_000001,0.0,15.5,0.0,highway,clear,50.0,0,0
frame_000002,0.1,15.6,0.1,highway,clear,48.5,0,0
frame_000003,0.2,15.7,0.2,highway,clear,47.0,1,0
```

**Required Columns:**
- `frame_id`: Frame identifier matching image filename
- `timestamp`: Time in seconds
- `ego_speed_mps`: Vehicle speed in meters per second
- `ego_yaw`: Vehicle yaw angle in degrees
- `road_type`: Road type (highway, urban, rural, etc.)
- `weather`: Weather condition (clear, rain, fog, snow, etc.)
- `lead_distance_m`: Distance to lead vehicle in meters
- `cut_in_flag`: Binary flag for cut-in events (0 or 1)
- `pedestrian_flag`: Binary flag for pedestrian presence (0 or 1)

## Architecture Overview

### Backend Components

- **FastAPI Server** (`app/main.py`): REST API endpoints
- **Database Models** (`app/models/`): SQLAlchemy ORM models
- **Services**:
  - `dataset_ingestion.py`: ZIP extraction and CSV parsing
  - `event_detector.py`: Rule-based scenario detection
  - `research_lab.py`: Multi-agent orchestration
- **Agents** (`app/agents/`):
  - `planner.py`: Research planning
  - `retriever.py`: Paper retrieval (mock)
  - `reader.py`: Information extraction
  - `critic.py`: Paper evaluation
  - `synthesizer.py`: Recommendation synthesis
  - `judge.py`: Lab comparison
  - `meta_learner.py`: Genome evolution

### Frontend Components

- **React + TypeScript + Vite**
- **TailwindCSS** for styling
- **Lucide React** for icons
- **Pages**:
  - `DatasetsPage`: Dataset list and upload
  - `DatasetDetailPage`: Event timeline and analysis
  - `StrategiesPage`: Genome evolution tracking

## API Endpoints

### Datasets
- `POST /api/upload-dataset` - Upload dataset ZIP
- `GET /api/datasets` - List all datasets
- `GET /api/datasets/{id}` - Get dataset details

### Events
- `GET /api/datasets/{id}/events` - List events for dataset

### Analysis
- `POST /api/datasets/{id}/events/{event_id}/analyze` - Run analysis
- `GET /api/datasets/{id}/events/{event_id}/analysis` - Get cached analysis

### Strategies
- `GET /api/labs/strategies` - Get all lab genome evolutions
- `GET /api/labs/{lab_name}/strategies` - Get specific lab evolution

## Troubleshooting

### Backend Issues

**Database not initialized:**
```bash
cd backend
python -m app.db.init_db
```

**Port already in use:**
```bash
# Change port in backend/.env or use different port
uvicorn app.main:app --reload --port 8001
```

### Frontend Issues

**API connection error:**
- Ensure backend is running on port 8000
- Check CORS settings in `backend/app/config.py`

**Build errors:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## Next Steps

### Extend with Real APIs

1. **Replace Mock LLM** (`app/agents/llm_client.py`):
   - Integrate OpenAI, Anthropic, or local LLM
   - Update `LLMClient` class

2. **Connect Research APIs** (`app/agents/retriever.py`):
   - arXiv API
   - Semantic Scholar API
   - Add API keys to `.env`

3. **Enable Forethought Integration** (`app/sponsors/forethought_incidents.py`):
   - Set `FORETHOUGHT_ENABLED=true` in `.env`
   - Add `FORETHOUGHT_API_KEY`

### Customize Genomes

Edit initial genomes in `backend/app/db/init_db.py`:
- Adjust keywords
- Modify critique dimensions
- Change venue weights
- Update year windows

## Support

For issues or questions:
- Check API docs: `http://localhost:8000/docs`
- Review logs in terminal
- Inspect browser console for frontend errors

## License

MIT License - See LICENSE file for details
