# Demo Datasets

This project includes 5 pre-generated demo datasets showcasing different autonomous driving scenarios.

## Available Datasets

### 1. Highway Cruise (150 frames)
- **Scenario**: Normal highway driving with lane changes and adaptive cruise control
- **Features**: 
  - Steady highway speeds (~25 m/s)
  - Lane change maneuvers
  - Following distance management
- **File**: `backend/storage/datasets/demos/highway_cruise.zip`

### 2. Urban Navigation (200 frames)
- **Scenario**: City driving with pedestrians, traffic lights, and intersections
- **Features**:
  - Lower urban speeds (~10 m/s)
  - Pedestrian detection and avoidance
  - Emergency braking for pedestrians
  - Complex urban environment
- **File**: `backend/storage/datasets/demos/urban_navigation.zip`

### 3. Emergency Braking (100 frames)
- **Scenario**: Sudden obstacle detection and emergency braking
- **Features**:
  - High-speed approach (~25 m/s)
  - Sudden obstacle appearance
  - Rapid deceleration
  - Critical safety event
- **File**: `backend/storage/datasets/demos/emergency_braking.zip`

### 4. Weather Adaptation (180 frames)
- **Scenario**: Driving through changing weather conditions
- **Features**:
  - Clear weather → Rain → Fog progression
  - Speed adaptation to conditions
  - Visibility challenges
  - Weather-based decision making
- **File**: `backend/storage/datasets/demos/weather_adaptation.zip`

### 5. Complex Merge (120 frames)
- **Scenario**: Highway merge with multiple vehicles and cut-in events
- **Features**:
  - Multiple vehicle interactions
  - Cut-in detection
  - Merge lane navigation
  - Dynamic traffic scenarios
- **File**: `backend/storage/datasets/demos/complex_merge.zip`

## How to Use

### Option 1: Upload via UI
1. Start the application with Docker: `docker-compose up -d`
2. Open http://localhost:5173
3. Click "Upload Dataset"
4. Select one of the demo ZIP files from `backend/storage/datasets/demos/`
5. Give it a name and upload

### Option 2: Generate New Datasets
```bash
# Generate all 5 demo datasets
python scripts/generate_demo_datasets.py

# The datasets will be created in backend/storage/datasets/demos/
```

### Option 3: Customize Generation
Edit `scripts/generate_demo_datasets.py` to:
- Add new scenarios
- Adjust frame counts
- Modify telemetry patterns
- Create custom events

## Dataset Structure

Each ZIP file contains:
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
frame_id,timestamp,ego_speed_mps,ego_yaw,road_type,weather,lead_distance_m,cut_in_flag,pedestrian_flag,brake_flag
frame_000001,0.0,25.0,0.0,highway,clear,50.0,0,0,0
...
```

## Analysis Workflow

1. **Upload Dataset**: Use the UI or API to upload a demo dataset
2. **Event Detection**: System automatically detects events (cut-ins, pedestrians, weather changes)
3. **Select Event**: Choose an event from the timeline
4. **Run Analysis**: Click "Run Analysis" to start the multi-agent system
5. **Monitor Agents**: Watch real-time agent activity in the right panel
6. **View Results**: Review comprehensive analysis with insights and recommendations

## Event Types Detected

- **cut_in**: Vehicle cutting into ego lane
- **pedestrian**: Pedestrian detection events
- **adverse_weather**: Weather condition changes
- **sudden_brake**: Emergency braking scenarios
- **lane_change**: Lane change maneuvers

## Next Steps

- Try uploading your own datasets following the same structure
- Experiment with different event types
- Analyze how the multi-agent system adapts its strategies
- View strategy evolution in the Strategies page
