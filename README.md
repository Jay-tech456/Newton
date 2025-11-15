<<<<<<< HEAD
# Newton
=======
# Autonomous Driving Data Preprocessing Pipeline

A comprehensive data preprocessing pipeline for autonomous driving datasets, designed to process .zip files containing images and CSV telemetry data, perform computer vision analysis using YOLO, and store results in a vector database for multi-agent interaction.

## 🚀 Features

- **Multi-format Data Ingestion**: Processes .zip files with images and CSV telemetry data
- **Advanced Image Analysis**: YOLO-based object detection with scene understanding
- **Vector Database Integration**: Pinecone integration for semantic search and agent queries
- **Real-time Processing**: Optimized for streaming data processing
- **Multi-agent Interface**: Structured API for agent interaction
- **Comprehensive Analysis**: Risk assessment, pattern detection, and safety insights

## 📋 Pipeline Components

### 1. Data Ingestion (`src/data_ingestion.py`)
- Extracts and processes .zip files
- Parses CSV telemetry data with validation
- Organizes data by frame_id for synchronization
- Mock data generation for testing

### 2. Image Analysis (`src/image_analysis.py`)
- YOLO object detection for vehicles, pedestrians, traffic signs
- Lane detection and road analysis
- Weather condition assessment
- Risk level evaluation
- Depth estimation for objects

### 3. Vector Database (`src/vector_database.py`)
- Pinecone integration for vector storage
- Text embedding generation using sentence transformers
- Semantic search capabilities
- Metadata-rich vector records

### 4. Main Pipeline (`src/main_pipeline.py`)
- Orchestrates all processing steps
- Handles real-time data processing
- Provides search and filtering capabilities
- Comprehensive statistics and monitoring

### 5. Agent Interface (`src/agent_interface.py`)
- Standardized query/response format
- Multiple agent types (safety, analysis, monitoring)
- Usage analytics and session management
- Extensible capability framework

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd autonomous-driving-pipeline
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your Pinecone credentials
```

4. **Download YOLO models** (automatic on first run)

## ⚙️ Configuration

Edit `config/config.yaml` to customize:

- **YOLO Model**: Choose model size (yolov8n.pt, yolov8s.pt, etc.)
- **Detection Classes**: Configure which objects to track
- **Vector Database**: Pinecone settings and dimensions
- **Processing Parameters**: Batch sizes, confidence thresholds
- **Real-time Settings**: Buffer sizes and processing intervals

## 🚗 Quick Start

### Basic Usage

```python
from src.main_pipeline import AutonomousDrivingPipeline

# Initialize pipeline
pipeline = AutonomousDrivingPipeline()

# Process a .zip file
results = pipeline.process_zip_file("path/to/your/data.zip")

# Process mock data for testing
results = pipeline.process_mock_data(num_frames=10)

# Search for similar frames
similar_frames = pipeline.search_frames("highway driving with pedestrians", top_k=10)

# Get high-risk frames
high_risk = pipeline.get_high_risk_frames(top_k=20)
```

### Multi-Agent Interface

```python
from src.agent_interface import MultiAgentInterface, create_safety_agent

# Initialize agent interface
agent_interface = MultiAgentInterface(pipeline)

# Create specialized agents
safety_agent = create_safety_agent(pipeline)

# Safety agent queries
high_risk_frames = safety_agent["get_high_risk"]()
risk_assessment = safety_agent["risk_assessment"]()

# Direct agent queries
response = agent_interface.handle_agent_query(
    agent_id="safety_monitor",
    query={
        "query_type": "search",
        "parameters": {
            "text": "cut-in situations on highway",
            "limit": 50
        }
    }
)
```

### Run Complete Example

```bash
python example_usage.py
```

## 📊 Data Format

### CSV Telemetry Data
```csv
frame_id,timestamp,ego_speed_mps,ego_yaw,road_type,weather,lead_distance_m,cut_in_flag,pedestrian_flag
1,0.00,27.0,0.01,highway,clear,35.0,0,0
2,0.10,27.1,0.01,highway,clear,32.0,1,0
```

### Image Requirements
- **Formats**: .jpg, .jpeg, .png, .bmp, .tiff
- **Naming**: Frame-based naming (e.g., `frame_1.jpg`, `image_001.jpg`)
- **Resolution**: Any size (automatically resized to 640x640)
- **Content**: Front-facing autonomous driving view

## 🤖 Agent Query Types

### 1. Search Queries
Semantic search using natural language:
```python
{
    "query_type": "search",
    "parameters": {
        "text": "pedestrian crossing at night",
        "limit": 20,
        "filters": {"risk_level": "high"}
    }
}
```

### 2. Filter Queries
Filter by specific criteria:
```python
{
    "query_type": "filter",
    "parameters": {
        "filter_type": "risk_level",
        "level": "high",
        "limit": 50
    }
}
```

### 3. Analysis Queries
Generate insights and patterns:
```python
{
    "query_type": "analysis",
    "parameters": {
        "analysis_type": "risk_assessment"
    }
}
```

### 4. Temporal Queries
Get time-based sequences:
```python
{
    "query_type": "temporal",
    "parameters": {
        "limit": 100
    }
}
```

### 5. Statistics Queries
Get pipeline and database statistics:
```python
{
    "query_type": "stats",
    "parameters": {
        "stats_type": "pipeline"
    }
}
```

## 🔍 Vector Database Schema

Each frame is stored as a vector with comprehensive metadata:

```python
{
    "id": "frame_123_1640995200",
    "vector": [0.1, 0.2, 0.3, ...],  # 1536-dimensional embedding
    "metadata": {
        "frame_id": "123",
        "timestamp": 1.23,
        "telemetry": {
            "ego_speed_mps": 25.5,
            "road_type": "highway",
            "weather": "clear",
            "cut_in_flag": false,
            "pedestrian_flag": false
        },
        "image_analysis": {
            "risk_level": "low",
            "obstacle_count": 3,
            "visibility_score": 0.85
        },
        "detections_summary": {
            "car": 2,
            "truck": 1
        },
        "search_tags": ["highway", "clear", "car", "truck"]
    }
}
```

## 📈 Real-time Processing

The pipeline supports real-time processing with:

- **Buffer Management**: Configurable buffer sizes for streaming data
- **Batch Processing**: Efficient batch uploads to vector database
- **Monitoring**: Real-time performance metrics and statistics
- **Error Handling**: Robust error recovery and logging

## 🛡️ Safety Features

### Risk Assessment
- **Multi-factor Analysis**: Speed, weather, obstacles, road type
- **Dynamic Risk Levels**: minimal, low, medium, high
- **Contextual Awareness**: Situation-based risk evaluation

### Object Detection
- **YOLO Integration**: State-of-the-art object detection
- **Custom Classes**: Vehicles, pedestrians, traffic signs, obstacles
- **Confidence Scoring**: Reliable detection with confidence thresholds

### Scene Understanding
- **Lane Detection**: Road lane analysis and width estimation
- **Weather Assessment**: Automatic weather condition detection
- **Visibility Analysis": Real-time visibility scoring

## 🔧 Advanced Configuration

### YOLO Model Configuration
```yaml
yolo:
  model_name: "yolov8n.pt"  # Nano for speed, use yolov8x.pt for accuracy
  confidence_threshold: 0.5
  iou_threshold: 0.45
  classes_to_track:
    - "person"
    - "car"
    - "truck"
    - "bus"
    - "traffic light"
```

### Vector Database Configuration
```yaml
pinecone:
  index_name: "autonomous-driving-frames"
  dimension: 1536
  metric: "cosine"
  batch_size: 100
```

### Real-time Settings
```yaml
realtime:
  buffer_size: 1000
  processing_interval: 0.1  # seconds
  enable_monitoring: true
```

## 📚 API Reference

### AutonomousDrivingPipeline

#### Methods
- `process_zip_file(zip_path: str) -> Dict`
- `process_csv_file(csv_path: str, image_dir: str) -> Dict`
- `process_mock_data(num_frames: int) -> Dict`
- `search_frames(query_text: str, top_k: int) -> List[Dict]`
- `get_high_risk_frames(top_k: int) -> List[Dict]`
- `get_pipeline_stats() -> Dict`

### MultiAgentInterface

#### Methods
- `handle_agent_query(agent_id: str, query: Dict) -> AgentResponse`
- `get_agent_capabilities() -> Dict`
- `get_agent_usage_stats() -> Dict`

## 🧪 Testing

### Mock Data Testing
```python
# Test with mock data
results = pipeline.process_mock_data(num_frames=10)
print(f"Processed {results['processing_summary']['total_frames']} frames")
```

### Agent Interface Testing
```python
# Test safety agent
safety_agent = create_safety_agent(pipeline)
response = safety_agent["get_high_risk"]()
print(f"Found {len(response.data)} high-risk frames")
```

## 🚀 Production Deployment

### Scalability Considerations
- **Vector Database**: Pinecone scales automatically
- **Processing**: Use GPU for YOLO inference
- **Storage**: Consider cloud storage for large image datasets
- **Monitoring**: Implement comprehensive logging and metrics

### Performance Optimization
- **Batch Processing**: Adjust batch sizes for your hardware
- **Model Selection**: Choose YOLO model based on speed/accuracy needs
- **Caching**: Cache frequently accessed results
- **Parallel Processing**: Utilize multiple cores for data ingestion

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

**Pinecone Connection Error**
```
Check your API key and environment in .env file
```

**YOLO Model Download Fails**
```
Ensure internet connection and try: pip install --upgrade ultralytics
```

**Memory Issues**
```
Reduce batch_size in config.yaml or use smaller YOLO model
```

**CUDA Out of Memory**
```
Set device: "cpu" in config.yaml or reduce image dimensions
```

### Support

- **Documentation**: Check inline code documentation
- **Examples**: See `example_usage.py` for comprehensive examples
- **Issues**: Create GitHub issue for bugs or feature requests

---

**Built for autonomous driving research and multi-agent AI systems** 🚗🤖
>>>>>>> 95fa201 (First commit for Data Preprocessing)
