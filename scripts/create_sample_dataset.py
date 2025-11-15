#!/usr/bin/env python3
"""
Create a sample dataset for testing AutoLab Drive.
Generates synthetic frames and telemetry data.
"""
import os
import csv
import zipfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import random

def create_sample_dataset(output_path: str = "sample_dataset.zip", num_frames: int = 100):
    """
    Create a sample dataset ZIP file.
    
    Args:
        output_path: Path to output ZIP file
        num_frames: Number of frames to generate
    """
    print(f"Creating sample dataset with {num_frames} frames...")
    
    # Create temporary directory
    temp_dir = Path("temp_dataset")
    temp_dir.mkdir(exist_ok=True)
    frames_dir = temp_dir / "frames"
    frames_dir.mkdir(exist_ok=True)
    
    # Generate frames
    print("Generating frames...")
    for i in range(1, num_frames + 1):
        frame_path = frames_dir / f"frame_{i:06d}.jpg"
        create_sample_frame(frame_path, i, num_frames)
        if i % 20 == 0:
            print(f"  Generated {i}/{num_frames} frames")
    
    # Generate telemetry
    print("Generating telemetry...")
    telemetry_path = temp_dir / "telemetry.csv"
    create_sample_telemetry(telemetry_path, num_frames)
    
    # Create ZIP
    print("Creating ZIP file...")
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in temp_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(temp_dir)
                zipf.write(file_path, arcname)
    
    # Cleanup
    print("Cleaning up...")
    import shutil
    shutil.rmtree(temp_dir)
    
    print(f"✓ Sample dataset created: {output_path}")
    print(f"  - {num_frames} frames")
    print(f"  - Telemetry CSV with synthetic events")
    print(f"  - File size: {os.path.getsize(output_path) / 1024 / 1024:.2f} MB")

def create_sample_frame(path: Path, frame_num: int, total_frames: int):
    """Create a sample frame image with text overlay."""
    # Create image
    img = Image.new('RGB', (640, 480), color=(50, 50, 50))
    draw = ImageDraw.Draw(img)
    
    # Draw road
    draw.rectangle([200, 200, 440, 480], fill=(80, 80, 80))
    draw.line([320, 200, 320, 480], fill=(255, 255, 0), width=3)
    
    # Draw horizon
    draw.line([0, 200, 640, 200], fill=(100, 150, 200), width=2)
    
    # Add frame number
    try:
        # Try to use default font, fallback to basic if not available
        font = ImageFont.load_default()
    except:
        font = None
    
    text = f"Frame {frame_num}/{total_frames}"
    draw.text((10, 10), text, fill=(255, 255, 255), font=font)
    
    # Add timestamp
    timestamp = frame_num * 0.1
    time_text = f"t={timestamp:.1f}s"
    draw.text((10, 30), time_text, fill=(255, 255, 255), font=font)
    
    # Save
    img.save(path, 'JPEG', quality=85)

def create_sample_telemetry(path: Path, num_frames: int):
    """Create sample telemetry CSV with synthetic events."""
    with open(path, 'w', newline='') as csvfile:
        fieldnames = [
            'frame_id', 'timestamp', 'ego_speed_mps', 'ego_yaw',
            'road_type', 'weather', 'lead_distance_m',
            'cut_in_flag', 'pedestrian_flag'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Generate telemetry data
        base_speed = 20.0  # m/s (~72 km/h)
        yaw = 0.0
        lead_distance = 50.0
        
        # Define event windows
        cut_in_start = 30
        cut_in_end = 35
        pedestrian_start = 60
        pedestrian_end = 65
        weather_change_start = 80
        
        for i in range(1, num_frames + 1):
            timestamp = (i - 1) * 0.1
            
            # Simulate speed variations
            speed = base_speed + random.uniform(-2, 2)
            
            # Simulate cut-in event (sudden lead distance decrease)
            if cut_in_start <= i <= cut_in_end:
                lead_distance = max(10.0, lead_distance - 5.0)
                cut_in_flag = 1
            else:
                lead_distance = min(50.0, lead_distance + 2.0)
                cut_in_flag = 0
            
            # Simulate pedestrian event
            pedestrian_flag = 1 if pedestrian_start <= i <= pedestrian_end else 0
            
            # Simulate weather change
            if i < weather_change_start:
                weather = 'clear'
            else:
                weather = 'rain'
            
            # Simulate lane change (yaw variation)
            if 45 <= i <= 50:
                yaw += 2.0
            elif 50 < i <= 55:
                yaw -= 2.0
            else:
                yaw += random.uniform(-0.5, 0.5)
            
            # Road type
            if i < 40:
                road_type = 'highway'
            elif i < 70:
                road_type = 'urban'
            else:
                road_type = 'highway'
            
            writer.writerow({
                'frame_id': f'frame_{i:06d}',
                'timestamp': round(timestamp, 1),
                'ego_speed_mps': round(speed, 1),
                'ego_yaw': round(yaw, 1),
                'road_type': road_type,
                'weather': weather,
                'lead_distance_m': round(lead_distance, 1),
                'cut_in_flag': cut_in_flag,
                'pedestrian_flag': pedestrian_flag
            })

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Create sample dataset for AutoLab Drive')
    parser.add_argument('--output', '-o', default='sample_dataset.zip',
                        help='Output ZIP file path (default: sample_dataset.zip)')
    parser.add_argument('--frames', '-n', type=int, default=100,
                        help='Number of frames to generate (default: 100)')
    
    args = parser.parse_args()
    
    create_sample_dataset(args.output, args.frames)
