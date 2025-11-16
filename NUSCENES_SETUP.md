# 🚗 nuScenes Dataset Setup Guide

## Quick Start (Recommended for Demo)

### 1. Download nuScenes Mini (2.5 GB)

Visit: https://www.nuscenes.org/nuscenes#download

Download **v1.0-mini** - Perfect for testing and demos!

```bash
# After downloading, extract:
tar -xzf v1.0-mini.tgz
```

### 2. Install nuScenes DevKit

```bash
pip install nuscenes-devkit
```

### 3. Convert to AutoLab Format

```bash
python scripts/convert_nuscenes.py \
    --nuscenes-path /path/to/v1.0-mini \
    --output backend/storage/datasets \
    --max-scenes 5
```

## What You'll Get

Each converted scene includes:
- **140-200 frames** from front camera
- **telemetry.csv** with vehicle state
- **metadata.json** with scene info
- **Automatic event detection** (pedestrians, vehicles, etc.)
- **ZIP file** ready to upload

## Example Output

```
backend/storage/datasets/
├── nuScenes_scene-0001/
│   ├── frames/
│   │   ├── frame_000000.jpg
│   │   ├── frame_000001.jpg
│   │   └── ...
│   ├── telemetry.csv
│   └── metadata.json
└── nuScenes_scene-0001.zip  ← Upload this!
```

## Full Dataset (Optional)

For production use, download the full dataset:

- **v1.0-trainval** (350 GB)
- 1000 scenes
- 1.4M camera images
- Full annotations

## Alternative: Use Our Synthetic Data

Already have 5 realistic datasets ready to use:
```
demo_datasets/
├── Urban_Pedestrian_Crossing.zip
├── Highway_Lane_Change.zip
├── Rainy_Emergency_Brake.zip
├── Suburban_Slow_Traffic.zip
└── Night_Urban_Navigation.zip
```

These are perfect for demos and don't require downloading nuScenes!

## Troubleshooting

### "nuscenes-devkit not found"
```bash
pip install nuscenes-devkit
```

### "Path not found"
Make sure you extracted the tar.gz file:
```bash
tar -xzf v1.0-mini.tgz
ls v1.0-mini/  # Should show: maps, samples, sweeps, v1.0-mini
```

### "Version mismatch"
Use the correct version flag:
```bash
--version v1.0-mini  # For mini dataset
--version v1.0-trainval  # For full dataset
```

## Next Steps

1. **Upload** the ZIP files at http://localhost:5173
2. **Analyze** events to see genome evolution
3. **Watch** SafetyLab vs PerformanceLab compete!

---

**Pro Tip**: Start with our synthetic datasets for quick demos, then add nuScenes for real-world validation! 🚀
