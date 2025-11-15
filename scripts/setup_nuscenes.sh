#!/bin/bash

echo "🚗 nuScenes Setup for AutoLab Drive"
echo "===================================="
echo ""

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 not found. Please install Python 3 first."
    exit 1
fi

# Install nuscenes-devkit
echo "📦 Installing nuscenes-devkit..."
pip3 install nuscenes-devkit

echo ""
echo "✅ Installation complete!"
echo ""
echo "📥 Next Steps:"
echo ""
echo "1. Download nuScenes Mini (2.5 GB):"
echo "   https://www.nuscenes.org/nuscenes#download"
echo ""
echo "2. Extract the dataset:"
echo "   tar -xzf v1.0-mini.tgz"
echo ""
echo "3. Convert to AutoLab format:"
echo "   python3 scripts/convert_nuscenes.py \\"
echo "       --nuscenes-path /path/to/v1.0-mini \\"
echo "       --output backend/storage/datasets \\"
echo "       --max-scenes 5"
echo ""
echo "4. Upload the ZIP files at http://localhost:5173"
echo ""
echo "📖 Full guide: NUSCENES_SETUP.md"
echo ""
