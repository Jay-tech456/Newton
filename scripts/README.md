# Scripts

Utility scripts for AutoLab Drive.

## create_sample_dataset.py

Creates a synthetic dataset for testing the system.

### Usage

```bash
# Create sample dataset with default settings (100 frames)
python scripts/create_sample_dataset.py

# Create larger dataset
python scripts/create_sample_dataset.py --frames 500 --output large_dataset.zip

# Custom output path
python scripts/create_sample_dataset.py -o my_test_data.zip -n 200
```

### Generated Dataset

The script creates:
- **Frames:** Synthetic road scene images (640x480 JPG)
- **Telemetry CSV:** With realistic driving data including:
  - Cut-in event around frame 30-35
  - Pedestrian event around frame 60-65
  - Weather change at frame 80
  - Lane change around frame 45-55
  - Speed and distance variations

### Requirements

```bash
pip install Pillow
```

### Output

Creates a ZIP file containing:
```
frames/
  frame_000001.jpg
  frame_000002.jpg
  ...
telemetry.csv
```

Ready to upload to AutoLab Drive!
