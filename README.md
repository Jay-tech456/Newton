# AutoLab Drive 

**A self-evolving multi-agent research system for autonomous driving**

AutoLab Drive is an offline research tool that analyzes real driving datasets using competing multi-agent labs (SafetyLab and PerformanceLab) that evolve their research strategies over time.

## 🎯 Features

- **Dataset Upload & Analysis**: Upload driving datasets (frames + telemetry CSV) for automated scenario detection
- **Multi-Agent Research Labs**: Two competing labs analyze each scenario with different priorities
  - **SafetyLab**: Focuses on robustness, rare events, and safety-critical scenarios
  - **PerformanceLab**: Emphasizes speed, SOTA metrics, and computational efficiency
- **Self-Evolution**: Labs evolve their research strategies based on Judge feedback
- **Visual Playback**: Frame-by-frame video playback with event timeline
- **Strategy Genome Tracking**: View evolution of research strategies over time

## 🏗️ Architecture

### Backend (Python + FastAPI)
- **Dataset Ingestion**: Parse ZIP files and CSV telemetry
- **Event Detection**: Identify cut-ins, pedestrians, adverse weather, etc.
- **Multi-Agent System**: 
  - Planner, Retriever, Reader, Critic, Synthesizer agents
  - Judge agent for comparing lab outputs
  - Meta-Learner for strategy evolution
- **Storage**: SQLite for metadata, filesystem for frames

### Frontend (React + TypeScript + Vite)
- Dataset upload interface
- Video-like frame playback
- Event timeline visualization
- Side-by-side lab comparison
- Strategy evolution timeline

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create storage directories
mkdir -p storage/datasets storage/frames

# Initialize database
python -m app.db.init_db

# Run server
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173` to access the UI.

## 📊 Dataset Format

### Directory Structure
```
dataset.zip
├── frames/
│   ├── frame_000001.jpg
│   ├── frame_000002.jpg
│   └── ...
└── telemetry.csv
```

### Telemetry CSV Format
```csv
frame_id,timestamp,ego_speed_mps,ego_yaw,road_type,weather,lead_distance_m,cut_in_flag,pedestrian_flag
frame_000001,0.0,15.5,0.0,highway,clear,50.0,0,0
frame_000002,0.1,15.6,0.1,highway,clear,48.5,0,0
...
```

## 🧬 Strategy Genome

Each lab maintains a strategy genome that defines:
- **Retrieval preferences**: Year windows, venue weights, keywords
- **Reading template**: Fields to extract from papers
- **Critique focus**: Dimensions to evaluate (safety vs performance)
- **Synthesis style**: Output format and audience

The Meta-Learner updates these genomes based on Judge feedback.

## 🤝 Sponsors Integration

- **Google DeepMind**: Method categorization (RL, imitation learning, model-based control)
- **Freepik**: Icon packs for visual elements (cars, weather, hazards)
- **Forethought**: Incident ticket simulation for real-world failure patterns

## 🔮 Future Extensions

- Connect to real research APIs (arXiv, Semantic Scholar)
- Integrate LiquidMetal AI or MCP Total for LLM capabilities
- Add more sophisticated evolution algorithms
- Support real-time streaming datasets
- Multi-modal analysis (LiDAR, radar)

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

Built with support from Google DeepMind, Freepik, and Forethought.
