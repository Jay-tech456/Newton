"""
Download and convert public autonomous driving datasets.
Supports: nuScenes, Waymo, KITTI, BDD100K
"""
import os
import json
import requests
from pathlib import Path

DATASETS = {
    "nuscenes": {
        "name": "nuScenes Mini",
        "url": "https://www.nuscenes.org/data/v1.0-mini.tgz",
        "size": "2.5 GB",
        "description": "Urban driving scenes with 3D annotations"
    },
    "kitti": {
        "name": "KITTI Raw Data",
        "url": "https://s3.eu-central-1.amazonaws.com/avg-kitti/raw_data/2011_09_26_drive_0001/2011_09_26_drive_0001_sync.zip",
        "size": "~1 GB",
        "description": "Urban and highway driving with stereo cameras"
    },
    "bdd100k": {
        "name": "BDD100K Sample",
        "url": "https://bdd-data.berkeley.edu/",
        "size": "Varies",
        "description": "Diverse weather and lighting conditions"
    }
}

def print_dataset_info():
    """Print information about available datasets."""
    print("🚗 Public Autonomous Driving Datasets\n")
    print("=" * 70)
    
    for key, info in DATASETS.items():
        print(f"\n📦 {info['name']}")
        print(f"   Size: {info['size']}")
        print(f"   Description: {info['description']}")
        print(f"   URL: {info['url']}")
    
    print("\n" + "=" * 70)
    print("\n💡 Quick Start Options:\n")
    print("1. **nuScenes Mini** (Recommended for demo)")
    print("   - Small size (2.5 GB)")
    print("   - High quality annotations")
    print("   - Urban scenarios")
    print("   - Download: https://www.nuscenes.org/nuscenes#download")
    
    print("\n2. **KITTI Raw Data** (Good for testing)")
    print("   - Medium size (~1 GB per sequence)")
    print("   - Stereo camera + lidar")
    print("   - Download: http://www.cvlibs.net/datasets/kitti/raw_data.php")
    
    print("\n3. **Waymo Open Dataset** (Most comprehensive)")
    print("   - Large size (requires registration)")
    print("   - Excellent quality")
    print("   - Download: https://waymo.com/open/download/")
    
    print("\n4. **BDD100K** (Most diverse)")
    print("   - Very large (requires registration)")
    print("   - Diverse conditions")
    print("   - Download: https://bdd-data.berkeley.edu/")
    
    print("\n" + "=" * 70)
    print("\n🔧 Conversion Tool:\n")
    print("After downloading, use our converter:")
    print("   python scripts/convert_public_dataset.py --dataset nuscenes --input /path/to/data")


def download_sample_urls():
    """Generate sample download commands."""
    print("\n📥 Sample Download Commands:\n")
    
    print("# nuScenes Mini (2.5 GB)")
    print("wget https://www.nuscenes.org/data/v1.0-mini.tgz")
    print("tar -xzf v1.0-mini.tgz")
    print()
    
    print("# KITTI Sample")
    print("wget https://s3.eu-central-1.amazonaws.com/avg-kitti/raw_data/2011_09_26_drive_0001/2011_09_26_drive_0001_sync.zip")
    print("unzip 2011_09_26_drive_0001_sync.zip")
    print()
    
    print("# Or use our automated downloader:")
    print("python scripts/download_public_datasets.py --auto")


def create_conversion_guide():
    """Create a guide for converting datasets."""
    guide = """
# Dataset Conversion Guide

## Converting Public Datasets to AutoLab Format

### Required Format:
```
dataset_name/
├── frames/
│   ├── frame_000000.jpg
│   ├── frame_000001.jpg
│   └── ...
├── telemetry.csv
└── metadata.json
```

### telemetry.csv Format:
```csv
frame_id,timestamp,ego_speed_mps,ego_yaw,road_type,weather,lead_distance_m,cut_in_flag,pedestrian_flag,brake_flag
frame_000000,0.0,21.69,0.0,highway,clear,35.0,0,0,0
```

### Conversion Steps:

#### 1. nuScenes
```python
# Extract frames from camera images
# Parse scene.json for telemetry
# Detect events from annotations
```

#### 2. KITTI
```python
# Extract frames from image sequences
# Parse oxts data for telemetry
# Use tracklets for event detection
```

#### 3. Waymo
```python
# Extract frames from TFRecord
# Parse vehicle state for telemetry
# Use labels for event detection
```

### Quick Converter (Coming Soon):
```bash
python scripts/convert_public_dataset.py \\
    --dataset nuscenes \\
    --input /path/to/nuscenes \\
    --output backend/storage/datasets/
```
"""
    
    guide_path = Path(__file__).parent.parent / "DATASET_CONVERSION_GUIDE.md"
    with open(guide_path, "w") as f:
        f.write(guide)
    
    print(f"\n✅ Created conversion guide: {guide_path}")


if __name__ == "__main__":
    print_dataset_info()
    print()
    download_sample_urls()
    print()
    create_conversion_guide()
    
    print("\n" + "=" * 70)
    print("\n🎯 Recommended for Quick Demo:\n")
    print("1. Use our generated datasets (already created!)")
    print("   Location: demo_datasets/")
    print()
    print("2. Or download nuScenes Mini for real data:")
    print("   - Visit: https://www.nuscenes.org/nuscenes#download")
    print("   - Download: v1.0-mini (2.5 GB)")
    print("   - Convert using our tool (coming soon)")
    print()
    print("3. For now, our synthetic datasets are perfect for demos!")
    print("   They have realistic scenarios and proper annotations.")
    print("\n" + "=" * 70)
