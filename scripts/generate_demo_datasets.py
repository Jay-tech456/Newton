#!/usr/bin/env python3
"""
Generate multiple demo datasets for AutoLab Drive.
Creates realistic autonomous driving scenarios with different conditions.
"""
import os
import sys
import csv
import zipfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import random
import math

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

DEMO_SCENARIOS = [
    {
        "name": "Highway Cruise",
        "description": "Normal highway driving with lane changes and adaptive cruise control",
        "frames": 150,
        "scenario": "highway_cruise"
    },
    {
        "name": "Urban Navigation",
        "description": "City driving with pedestrians, traffic lights, and intersections",
        "frames": 200,
        "scenario": "urban_navigation"
    },
    {
        "name": "Emergency Braking",
        "description": "Sudden obstacle detection and emergency braking scenario",
        "frames": 100,
        "scenario": "emergency_braking"
    },
    {
        "name": "Weather Adaptation",
        "description": "Driving through changing weather conditions (clear to rain to fog)",
        "frames": 180,
        "scenario": "weather_adaptation"
    },
    {
        "name": "Complex Merge",
        "description": "Highway merge with multiple vehicles and cut-in events",
        "frames": 120,
        "scenario": "complex_merge"
    }
]

def create_frame(path: Path, frame_num: int, total_frames: int, scenario: str):
    """Create a frame based on scenario."""
    img = Image.new('RGB', (800, 600), color=(50, 50, 50))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    
    progress = frame_num / total_frames
    
    if scenario == "highway_cruise":
        draw_highway_scene(draw, frame_num, progress)
    elif scenario == "urban_navigation":
        draw_urban_scene(draw, frame_num, progress)
    elif scenario == "emergency_braking":
        draw_emergency_scene(draw, frame_num, progress)
    elif scenario == "weather_adaptation":
        draw_weather_scene(draw, frame_num, progress)
    elif scenario == "complex_merge":
        draw_merge_scene(draw, frame_num, progress)
    
    # Add ego vehicle (self-driving car) at bottom
    draw_ego_vehicle(draw, frame_num)
    
    # Add HUD overlay
    draw_hud(draw, font, frame_num, total_frames)
    
    img.save(path, 'JPEG', quality=90)

def draw_ego_vehicle(draw, frame_num):
    """Draw the ego vehicle (self-driving car) at the bottom center."""
    # Car body - main rectangle
    car_x = 320
    car_y = 520
    car_width = 160
    car_height = 70
    
    # Car body (blue autonomous vehicle)
    draw.rectangle([car_x, car_y, car_x + car_width, car_y + car_height], 
                   fill=(30, 100, 200), outline=(20, 70, 150), width=3)
    
    # Windshield
    draw.polygon([
        (car_x + 20, car_y + 10),
        (car_x + car_width - 20, car_y + 10),
        (car_x + car_width - 30, car_y - 10),
        (car_x + 30, car_y - 10)
    ], fill=(100, 150, 220), outline=(50, 100, 180), width=2)
    
    # Wheels
    wheel_y = car_y + car_height - 5
    # Left wheel
    draw.ellipse([car_x + 20, wheel_y, car_x + 45, wheel_y + 15], 
                 fill=(40, 40, 40), outline=(20, 20, 20), width=2)
    # Right wheel
    draw.ellipse([car_x + car_width - 45, wheel_y, car_x + car_width - 20, wheel_y + 15], 
                 fill=(40, 40, 40), outline=(20, 20, 20), width=2)
    
    # Headlights
    draw.ellipse([car_x + 10, car_y + 20, car_x + 25, car_y + 30], 
                 fill=(255, 255, 200), outline=(200, 200, 150), width=1)
    draw.ellipse([car_x + car_width - 25, car_y + 20, car_x + car_width - 10, car_y + 30], 
                 fill=(255, 255, 200), outline=(200, 200, 150), width=1)
    
    # Autonomous driving indicator (glowing sensor on top)
    sensor_x = car_x + car_width // 2
    sensor_y = car_y - 15
    # Sensor dome
    draw.ellipse([sensor_x - 15, sensor_y - 10, sensor_x + 15, sensor_y + 10], 
                 fill=(0, 255, 150), outline=(0, 200, 100), width=2)
    # Pulsing glow effect
    glow_size = 5 + int(math.sin(frame_num * 0.3) * 3)
    draw.ellipse([sensor_x - glow_size, sensor_y - glow_size, 
                  sensor_x + glow_size, sensor_y + glow_size], 
                 fill=(100, 255, 200), outline=(50, 255, 150), width=1)
    
    # "AUTONOMOUS" label
    try:
        font = ImageFont.load_default()
        draw.text((car_x + 45, car_y + 35), "AUTO", fill=(255, 255, 255), font=font)
    except:
        pass

def draw_highway_scene(draw, frame_num, progress):
    """Draw highway scene."""
    # Sky
    draw.rectangle([0, 0, 800, 250], fill=(100, 150, 200))
    
    # Road
    draw.rectangle([200, 250, 600, 600], fill=(60, 60, 60))
    
    # Lane markings
    for i in range(5):
        y = 250 + (i * 70) - (frame_num * 10 % 70)
        draw.rectangle([395, y, 405, y + 40], fill=(255, 255, 0))
    
    # Side barriers
    draw.line([200, 250, 200, 600], fill=(200, 200, 200), width=3)
    draw.line([600, 250, 600, 600], fill=(200, 200, 200), width=3)
    
    # Lead vehicle (if present)
    if progress < 0.7:
        lead_y = 300 + int(math.sin(frame_num * 0.1) * 20)
        draw.rectangle([350, lead_y, 450, lead_y + 60], fill=(200, 50, 50))

def draw_urban_scene(draw, frame_num, progress):
    """Draw urban scene with buildings and pedestrians."""
    # Sky
    draw.rectangle([0, 0, 800, 200], fill=(120, 160, 220))
    
    # Buildings
    for i in range(5):
        x = i * 160
        height = random.randint(100, 180)
        draw.rectangle([x, 200 - height, x + 140, 200], fill=(80, 80, 100))
    
    # Road
    draw.rectangle([0, 350, 800, 600], fill=(70, 70, 70))
    
    # Crosswalk
    if 0.3 < progress < 0.5:
        for i in range(10):
            x = i * 80
            draw.rectangle([x, 400, x + 40, 450], fill=(255, 255, 255))
    
    # Pedestrian
    if 0.35 < progress < 0.45:
        ped_x = 300 + int((progress - 0.35) * 2000)
        draw.ellipse([ped_x, 380, ped_x + 30, 410], fill=(255, 200, 150))
        draw.rectangle([ped_x + 5, 410, ped_x + 25, 450], fill=(50, 50, 200))

def draw_emergency_scene(draw, frame_num, progress):
    """Draw emergency braking scenario."""
    # Sky
    draw.rectangle([0, 0, 800, 250], fill=(100, 150, 200))
    
    # Road
    draw.rectangle([200, 250, 600, 600], fill=(60, 60, 60))
    
    # Obstacle appears suddenly
    if progress > 0.4:
        obstacle_y = 280 + int((progress - 0.4) * 300)
        # Red warning box
        draw.rectangle([340, obstacle_y - 10, 460, obstacle_y + 70], 
                      outline=(255, 0, 0), width=5)
        # Obstacle
        draw.rectangle([350, obstacle_y, 450, obstacle_y + 50], fill=(150, 150, 0))

def draw_weather_scene(draw, frame_num, progress):
    """Draw scene with changing weather."""
    # Sky color changes
    if progress < 0.33:
        sky_color = (100, 150, 200)  # Clear
    elif progress < 0.66:
        sky_color = (80, 80, 100)  # Rain
    else:
        sky_color = (150, 150, 150)  # Fog
    
    draw.rectangle([0, 0, 800, 250], fill=sky_color)
    
    # Road
    draw.rectangle([200, 250, 600, 600], fill=(60, 60, 60))
    
    # Rain effect
    if 0.33 < progress < 0.66:
        for _ in range(50):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            draw.line([x, y, x + 2, y + 10], fill=(200, 200, 255), width=1)
    
    # Fog effect
    if progress > 0.66:
        overlay = Image.new('RGBA', (800, 600), (200, 200, 200, 100))
        # Note: This is simplified; in real implementation would blend

def draw_merge_scene(draw, frame_num, progress):
    """Draw highway merge scenario."""
    # Sky
    draw.rectangle([0, 0, 800, 250], fill=(100, 150, 200))
    
    # Main road
    draw.rectangle([200, 250, 600, 600], fill=(60, 60, 60))
    
    # Merge lane
    merge_width = int(150 * (1 - progress))
    if merge_width > 0:
        draw.polygon([600, 250, 750, 250, 600, 400], fill=(70, 70, 70))
    
    # Multiple vehicles
    vehicles = [
        (350, 320, (200, 50, 50)),
        (420, 380, (50, 200, 50)),
        (280, 450, (50, 50, 200))
    ]
    
    for x, y, color in vehicles:
        y_offset = int(math.sin(frame_num * 0.05 + x) * 10)
        draw.rectangle([x, y + y_offset, x + 60, y + y_offset + 40], fill=color)

def draw_hud(draw, font, frame_num, total_frames):
    """Draw heads-up display overlay."""
    timestamp = frame_num * 0.1
    
    # Frame info
    draw.text((10, 10), f"Frame: {frame_num}/{total_frames}", fill=(0, 255, 0), font=font)
    draw.text((10, 30), f"Time: {timestamp:.1f}s", fill=(0, 255, 0), font=font)
    
    # Speed indicator
    speed = 20 + random.uniform(-2, 2)
    draw.text((10, 560), f"Speed: {speed:.1f} m/s", fill=(0, 255, 0), font=font)

def create_telemetry(path: Path, num_frames: int, scenario: str):
    """Create telemetry CSV based on scenario."""
    with open(path, 'w', newline='') as csvfile:
        fieldnames = [
            'frame_id', 'timestamp', 'ego_speed_mps', 'ego_yaw',
            'road_type', 'weather', 'lead_distance_m',
            'cut_in_flag', 'pedestrian_flag', 'brake_flag'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for i in range(1, num_frames + 1):
            progress = i / num_frames
            timestamp = (i - 1) * 0.1
            
            row = generate_telemetry_row(i, timestamp, progress, scenario)
            writer.writerow(row)

def generate_telemetry_row(frame_num, timestamp, progress, scenario):
    """Generate telemetry row based on scenario."""
    base_row = {
        'frame_id': f'frame_{frame_num:06d}',
        'timestamp': round(timestamp, 1),
        'ego_speed_mps': 20.0,
        'ego_yaw': 0.0,
        'road_type': 'highway',
        'weather': 'clear',
        'lead_distance_m': 50.0,
        'cut_in_flag': 0,
        'pedestrian_flag': 0,
        'brake_flag': 0
    }
    
    if scenario == "highway_cruise":
        base_row['ego_speed_mps'] = 25.0 + random.uniform(-1, 1)
        if 0.3 < progress < 0.5:
            base_row['ego_yaw'] = 5.0  # Lane change
        base_row['lead_distance_m'] = 40.0 + random.uniform(-5, 5)
        
    elif scenario == "urban_navigation":
        base_row['road_type'] = 'urban'
        base_row['ego_speed_mps'] = 10.0 + random.uniform(-2, 2)
        if 0.35 < progress < 0.45:
            base_row['pedestrian_flag'] = 1
            base_row['brake_flag'] = 1
            base_row['ego_speed_mps'] = max(0, 10.0 - (progress - 0.35) * 100)
        
    elif scenario == "emergency_braking":
        base_row['ego_speed_mps'] = 25.0
        if progress > 0.4:
            base_row['brake_flag'] = 1
            base_row['lead_distance_m'] = max(5.0, 50.0 - (progress - 0.4) * 150)
            base_row['ego_speed_mps'] = max(0, 25.0 - (progress - 0.4) * 60)
        else:
            base_row['lead_distance_m'] = 50.0
            
    elif scenario == "weather_adaptation":
        if progress < 0.33:
            base_row['weather'] = 'clear'
            base_row['ego_speed_mps'] = 25.0
        elif progress < 0.66:
            base_row['weather'] = 'rain'
            base_row['ego_speed_mps'] = 18.0
        else:
            base_row['weather'] = 'fog'
            base_row['ego_speed_mps'] = 12.0
            
    elif scenario == "complex_merge":
        base_row['ego_speed_mps'] = 22.0 + random.uniform(-2, 2)
        if 0.3 < progress < 0.5:
            base_row['cut_in_flag'] = 1
            base_row['lead_distance_m'] = 15.0
        else:
            base_row['lead_distance_m'] = 35.0
    
    return base_row

def create_dataset(scenario_info, output_dir):
    """Create a single dataset."""
    name = scenario_info["name"]
    num_frames = scenario_info["frames"]
    scenario = scenario_info["scenario"]
    
    print(f"\n📦 Creating dataset: {name}")
    print(f"   Scenario: {scenario}, Frames: {num_frames}")
    
    # Create temporary directory
    temp_dir = Path("temp_dataset")
    temp_dir.mkdir(exist_ok=True)
    frames_dir = temp_dir / "frames"
    frames_dir.mkdir(exist_ok=True)
    
    # Generate frames
    print("   Generating frames...")
    for i in range(1, num_frames + 1):
        frame_path = frames_dir / f"frame_{i:06d}.jpg"
        create_frame(frame_path, i, num_frames, scenario)
        if i % 50 == 0:
            print(f"     {i}/{num_frames} frames")
    
    # Generate telemetry
    print("   Generating telemetry...")
    telemetry_path = temp_dir / "telemetry.csv"
    create_telemetry(telemetry_path, num_frames, scenario)
    
    # Create ZIP
    output_path = output_dir / f"{scenario}.zip"
    print("   Creating ZIP file...")
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in temp_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(temp_dir)
                zipf.write(file_path, arcname)
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)
    
    size_mb = os.path.getsize(output_path) / 1024 / 1024
    print(f"   ✓ Created: {output_path.name} ({size_mb:.2f} MB)")
    
    return output_path

def main():
    """Generate all demo datasets."""
    print("=" * 60)
    print("AutoLab Drive - Demo Dataset Generator")
    print("=" * 60)
    
    # Create output directory
    output_dir = Path(__file__).parent.parent / "backend" / "storage" / "datasets" / "demos"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nOutput directory: {output_dir}")
    print(f"Generating {len(DEMO_SCENARIOS)} demo datasets...\n")
    
    created_files = []
    for scenario in DEMO_SCENARIOS:
        try:
            output_path = create_dataset(scenario, output_dir)
            created_files.append(output_path)
        except Exception as e:
            print(f"   ✗ Error: {e}")
    
    print("\n" + "=" * 60)
    print(f"✓ Successfully created {len(created_files)} demo datasets")
    print("=" * 60)
    print("\nCreated files:")
    for file_path in created_files:
        print(f"  - {file_path.name}")
    
    print("\n📝 To use these datasets:")
    print("   1. Upload them through the AutoLab Drive UI")
    print("   2. Or copy them to: backend/storage/datasets/")
    print("   3. The system will automatically process them")

if __name__ == "__main__":
    main()
