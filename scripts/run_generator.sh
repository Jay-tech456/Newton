#!/bin/bash

echo "🚗 Generating Realistic Driving Datasets..."
echo ""

cd "$(dirname "$0")"

# Install PIL if needed
pip install -q Pillow numpy

# Run the generator
python3 generate_realistic_dataset.py

echo ""
echo "✅ Done! Datasets are ready in backend/storage/datasets/"
