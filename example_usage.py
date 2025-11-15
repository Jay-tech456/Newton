"""
Example Usage of Autonomous Driving Data Pipeline
Demonstrates how to use the complete system for data preprocessing and agent interaction
"""

import os
from dotenv import load_dotenv
from src.main_pipeline import AutonomousDrivingPipeline
from src.agent_interface import MultiAgentInterface, create_safety_agent, create_analysis_agent

# Load environment variables
load_dotenv()

def main():
    """Complete example of pipeline usage"""
    print("🚗 Autonomous Driving Data Pipeline Example\n")
    
    # Initialize the pipeline
    print("1. Initializing pipeline...")
    pipeline = AutonomousDrivingPipeline()
    
    # Example 1: Process mock data (since we don't have real data)
    print("\n2. Processing mock autonomous driving data...")
    results = pipeline.process_mock_data(num_frames=10)
    
    print(f"✅ Processed {results['processing_summary']['total_frames']} frames")
    print(f"   - Images analyzed: {results['processing_summary']['frames_analyzed']}")
    print(f"   - Vectors stored: {results['processing_summary']['vectors_stored']}")
    print(f"   - Processing time: {results['processing_summary']['processing_time_seconds']:.2f}s")
    
    # Example 2: Initialize multi-agent interface
    print("\n3. Setting up multi-agent interface...")
    agent_interface = MultiAgentInterface(pipeline)
    
    # Example 3: Create specialized agents
    print("\n4. Creating specialized agents...")
    safety_agent = create_safety_agent(pipeline)
    analysis_agent = create_analysis_agent(pipeline)
    
    # Example 4: Agent queries - Safety Agent
    print("\n5. Safety Agent Examples:")
    print("   a) Getting high-risk frames...")
    high_risk_response = safety_agent["get_high_risk"]()
    if high_risk_response.success:
        print(f"      Found {len(high_risk_response.data)} high-risk frames")
    
    print("   b) Searching for pedestrian situations...")
    pedestrian_response = safety_agent["query"]("pedestrian crossing situations")
    if pedestrian_response.success:
        print(f"      Found {len(pedestrian_response.data)} pedestrian-related frames")
    
    print("   c) Getting risk assessment...")
    risk_assessment = safety_agent["risk_assessment"]()
    if risk_assessment.success:
        print(f"      High risk situations: {risk_assessment.data['high_risk_count']}")
        print(f"      Risk factors: {list(risk_assessment.data['risk_factors'][:3])}")
    
    # Example 5: Agent queries - Analysis Agent
    print("\n6. Analysis Agent Examples:")
    print("   a) Analyzing cut-in situations...")
    cut_in_analysis = analysis_agent["analyze"]("cut in maneuver")
    if cut_in_analysis.success:
        print(f"      Found {len(cut_in_analysis.data)} cut-in situations")
    
    print("   b) Getting pattern analysis...")
    patterns = analysis_agent["get_patterns"]()
    if patterns.success:
        print(f"      Common situations: {list(patterns.data['frequent_situations'].items())[:3]}")
    
    print("   c) Getting summary analysis...")
    summary = analysis_agent["get_summary"]()
    if summary.success:
        print(f"      Average speed: {summary.data['average_speed']:.1f} m/s")
        print(f"      Risk distribution: {summary.data['risk_level_distribution']}")
    
    # Example 6: Direct agent interface queries
    print("\n7. Direct Agent Interface Examples:")
    
    # Semantic search
    search_response = agent_interface.handle_agent_query(
        agent_id="research_agent",
        query={
            "query_type": "search",
            "parameters": {
                "text": "highway driving in rainy weather",
                "limit": 5
            }
        }
    )
    if search_response.success:
        print(f"   Search results: {len(search_response.data)} frames found")
        print(f"   Response time: {search_response.response_time_ms:.1f}ms")
    
    # Filter by conditions
    filter_response = agent_interface.handle_agent_query(
        agent_id="monitoring_agent",
        query={
            "query_type": "filter",
            "parameters": {
                "filter_type": "telemetry",
                "conditions": {
                    "speed_range": [20, 30],
                    "road_types": ["highway"]
                },
                "limit": 10
            }
        }
    )
    if filter_response.success:
        print(f"   Filtered results: {len(filter_response.data)} frames matching criteria")
    
    # Get statistics
    stats_response = agent_interface.handle_agent_query(
        agent_id="admin_agent",
        query={
            "query_type": "stats",
            "parameters": {
                "stats_type": "pipeline"
            }
        }
    )
    if stats_response.success:
        stats = stats_response.data
        print(f"   Total frames processed: {stats['total_frames_processed']}")
        print(f"   Total vectors stored: {stats['total_vectors_stored']}")
        print(f"   Pipeline runtime: {stats['pipeline_runtime_seconds']:.1f}s")
    
    # Example 7: Agent capabilities
    print("\n8. Agent Capabilities:")
    capabilities = agent_interface.get_agent_capabilities()
    print("   Available query types:")
    for query_type in capabilities['query_types']:
        print(f"      - {query_type['type']}: {query_type['description']}")
    
    print("   Available filters:")
    for category, options in capabilities['filter_options'].items():
        print(f"      - {category}: {options[:3]}...")
    
    # Example 8: Show agent usage statistics
    print("\n9. Agent Usage Statistics:")
    usage_stats = agent_interface.handle_agent_query(
        agent_id="admin_agent",
        query={
            "query_type": "stats",
            "parameters": {
                "stats_type": "agent_usage"
            }
        }
    )
    if usage_stats.success:
        usage = usage_stats.data
        print(f"   Total queries: {usage['total_queries']}")
        print(f"   Active agents: {usage['active_agents']}")
        print(f"   Average response time: {usage['average_response_time_ms']:.1f}ms")
    
    # Cleanup
    print("\n10. Cleaning up...")
    pipeline.cleanup_temp_files()
    
    print("\n✨ Example completed successfully!")
    print("\nNext steps:")
    print("1. Set up your Pinecone API key in .env file")
    print("2. Replace mock data with real .zip files containing images + CSV")
    print("3. Customize the YOLO model and image analysis parameters")
    print("4. Integrate with your existing multi-agent system")

def create_sample_data():
    """Create sample data for testing"""
    print("\n📁 Creating sample data structure...")
    
    # Create directories
    os.makedirs("data/input", exist_ok=True)
    os.makedirs("data/output", exist_ok=True)
    os.makedirs("data/temp", exist_ok=True)
    
    # Create sample CSV
    sample_csv = """frame_id,timestamp,ego_speed_mps,ego_yaw,road_type,weather,lead_distance_m,cut_in_flag,pedestrian_flag
1,0.00,25.5,0.01,highway,clear,35.0,0,0
2,0.10,26.0,0.02,highway,clear,32.0,1,0
3,0.20,25.8,0.01,highway,clear,30.0,0,1
4,0.30,27.2,0.03,urban,clear,15.0,0,0
5,0.40,24.5,0.02,urban,rainy,12.0,1,1
6,0.50,26.8,0.01,highway,clear,40.0,0,0
7,0.60,28.0,0.02,highway,clear,38.0,0,0
8,0.70,22.0,0.05,urban,rainy,10.0,1,0
9,0.80,24.2,0.03,urban,clear,18.0,0,1
10,0.90,26.5,0.01,highway,clear,42.0,0,0"""
    
    with open("data/input/sample_telemetry.csv", "w") as f:
        f.write(sample_csv)
    
    print("   ✅ Sample CSV created: data/input/sample_telemetry.csv")
    print("   📂 Data directories created")

def setup_environment():
    """Setup environment file with required variables"""
    print("\n⚙️ Setting up environment...")
    
    env_content = """# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=your_pinecone_environment_here

# Optional: GPU Configuration
# CUDA_VISIBLE_DEVICES=0"""
    
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write(env_content)
        print("   ✅ Created .env file")
        print("   ⚠️  Please update with your Pinecone API key")
    else:
        print("   ✅ .env file already exists")
    
    print("\n📋 Setup instructions:")
    print("1. Get your Pinecone API key from https://app.pinecone.io")
    print("2. Update the .env file with your credentials")
    print("3. Install dependencies: pip install -r requirements.txt")
    print("4. Run the example: python example_usage.py")

if __name__ == "__main__":
    print("🚗 Autonomous Driving Data Pipeline - Setup & Example\n")
    
    # Setup environment and sample data
    setup_environment()
    create_sample_data()
    
    # Ask user if they want to run the example
    user_input = input("\n🤖 Would you like to run the full example? (y/n): ").lower().strip()
    
    if user_input in ['y', 'yes']:
        try:
            main()
        except Exception as e:
            print(f"\n❌ Error running example: {e}")
            print("\n🔧 Troubleshooting:")
            print("1. Make sure you've installed all dependencies: pip install -r requirements.txt")
            print("2. Check your Pinecone API key in .env file")
            print("3. Ensure you have internet connection for downloading models")
    else:
        print("\n💡 Ready to start! When you're ready to run the example:")
        print("   python example_usage.py")
        print("\n📚 For more details, see the documentation in each module.")