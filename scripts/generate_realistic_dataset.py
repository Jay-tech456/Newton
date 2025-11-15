"""
Generate realistic autonomous driving dataset with various scenarios.
Creates video frames and event annotations for testing.
"""
import os
import json
import random
import shutil
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Realistic driving scenarios
SCENARIOS = [
    {
        "name": "Urban Pedestrian Crossing",
        "event_type": "pedestrian",
        "severity": "high",
        "description": "Pedestrian suddenly crosses street in urban area",
        "ego_speed_mps": 8.3,  # 30 km/h
        "road_type": "urban",
        "weather": "clear",
        "lead_distance_m": 15.0,
        "cut_in_flag": False,
        "frame_range": (30, 90),
        "num_events": 2
    },
    {
        "name": "Highway Lane Change",
        "event_type": "cut_in",
        "severity": "medium",
        "description": "Vehicle cuts into lane on highway",
        "ego_speed_mps": 27.8,  # 100 km/h
        "road_type": "highway",
        "weather": "clear",
        "lead_distance_m": 25.0,
        "cut_in_flag": True,
        "frame_range": (40, 100),
        "num_events": 3
    },
    {
        "name": "Rainy Emergency Brake",
        "event_type": "emergency_brake",
        "severity": "high",
        "description": "Emergency braking in rainy conditions",
        "ego_speed_mps": 16.7,  # 60 km/h
        "road_type": "highway",
        "weather": "rain",
        "lead_distance_m": 12.0,
        "cut_in_flag": False,
        "frame_range": (20, 70),
        "num_events": 2
    },
    {
        "name": "Suburban Slow Traffic",
        "event_type": "slow_lead",
        "severity": "low",
        "description": "Following slow vehicle in suburban area",
        "ego_speed_mps": 11.1,  # 40 km/h
        "road_type": "suburban",
        "weather": "clear",
        "lead_distance_m": 20.0,
        "cut_in_flag": False,
        "frame_range": (50, 150),
        "num_events": 1
    },
    {
        "name": "Night Urban Navigation",
        "event_type": "pedestrian",
        "severity": "medium",
        "description": "Pedestrian detection at night in urban area",
        "ego_speed_mps": 6.9,  # 25 km/h
        "road_type": "urban",
        "weather": "night",
        "lead_distance_m": 18.0,
        "cut_in_flag": False,
        "frame_range": (35, 95),
        "num_events": 2
    }
]


def create_frame(frame_num, scenario, total_frames, event_active=False):
    """Create a single video frame with scenario visualization."""
    # Create image
    width, height = 1280, 720
    img = Image.new('RGB', (width, height), color=(50, 50, 60))
    draw = ImageDraw.Draw(img)
    
    # Draw road
    road_y = height * 0.6
    draw.rectangle([0, road_y, width, height], fill=(40, 40, 45))
    
    # Draw lane markings
    for i in range(0, width, 100):
        draw.rectangle([i, road_y + height * 0.15, i + 50, road_y + height * 0.17], fill=(200, 200, 200))
    
    # Draw horizon
    draw.line([(0, road_y), (width, road_y)], fill=(100, 100, 110), width=3)
    
    # Add weather effects
    if scenario["weather"] == "rain":
        for _ in range(200):
            x = random.randint(0, width)
            y = random.randint(0, height)
            draw.line([(x, y), (x + 2, y + 10)], fill=(150, 150, 200), width=1)
    elif scenario["weather"] == "night":
        # Darken the image slightly for night effect
        img = Image.blend(img, Image.new('RGB', (width, height), color=(10, 10, 20)), 0.3)
        draw = ImageDraw.Draw(img)
        
        # Add headlight beams
        for i in range(3):
            beam_x = width//2 + (i - 1) * 100
            draw.polygon([(beam_x - 30, height - 100), (beam_x + 30, height - 100), 
                         (beam_x + 80, road_y), (beam_x - 80, road_y)], 
                        fill=(255, 255, 200, 40), outline=(255, 255, 150))
    
    # Draw ego vehicle indicator
    draw.rectangle([width//2 - 40, height - 100, width//2 + 40, height - 20], 
                   fill=(0, 150, 255), outline=(255, 255, 255), width=2)
    
    # Draw lead vehicle or pedestrian if event is active
    if event_active:
        progress = (frame_num - scenario["frame_range"][0]) / (scenario["frame_range"][1] - scenario["frame_range"][0])
        
        if scenario["event_type"] == "pedestrian":
            # Draw pedestrian
            ped_x = width//2 + int((progress - 0.5) * 200)
            ped_y = road_y - 80
            draw.ellipse([ped_x - 15, ped_y - 30, ped_x + 15, ped_y], fill=(200, 100, 100))
            draw.rectangle([ped_x - 10, ped_y, ped_x + 10, ped_y + 40], fill=(100, 100, 200))
            
            # Warning box
            draw.rectangle([ped_x - 25, ped_y - 40, ped_x + 25, ped_y + 50], 
                          outline=(255, 0, 0), width=3)
        else:
            # Draw lead vehicle
            lead_x = width//2
            lead_y = road_y - int(scenario["lead_distance_m"] * 3)
            draw.rectangle([lead_x - 35, lead_y - 60, lead_x + 35, lead_y], 
                          fill=(150, 150, 150), outline=(255, 255, 255), width=2)
            
            if scenario["event_type"] == "emergency_brake":
                # Red brake lights
                draw.rectangle([lead_x - 30, lead_y - 10, lead_x - 15, lead_y], fill=(255, 0, 0))
                draw.rectangle([lead_x + 15, lead_y - 10, lead_x + 30, lead_y], fill=(255, 0, 0))
    
    # Add HUD overlay
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Speed indicator
    speed_kmh = int(scenario["ego_speed_mps"] * 3.6)
    draw.rectangle([20, 20, 200, 100], fill=(0, 0, 0, 180), outline=(0, 200, 255), width=2)
    draw.text((30, 30), f"Speed: {speed_kmh} km/h", fill=(0, 200, 255), font=font)
    draw.text((30, 60), f"Frame: {frame_num}/{total_frames}", fill=(200, 200, 200), font=small_font)
    
    # Event indicator
    if event_active:
        draw.rectangle([width - 220, 20, width - 20, 80], 
                      fill=(255, 0, 0, 180), outline=(255, 255, 0), width=3)
        draw.text((width - 210, 30), "⚠ EVENT", fill=(255, 255, 0), font=font)
        draw.text((width - 210, 55), scenario["event_type"].upper(), fill=(255, 255, 255), font=small_font)
    
    return img


def generate_dataset(output_dir, scenario):
    """Generate a complete dataset for a scenario."""
    dataset_name = f"{scenario['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    dataset_path = os.path.join(output_dir, dataset_name)
    frames_path = os.path.join(dataset_path, "frames")
    
    os.makedirs(frames_path, exist_ok=True)
    
    # Generate frames
    total_frames = scenario["frame_range"][1] + 50
    events = []
    
    print(f"Generating {total_frames} frames for '{scenario['name']}'...")
    
    for frame_num in range(total_frames):
        event_active = scenario["frame_range"][0] <= frame_num <= scenario["frame_range"][1]
        
        # Create and save frame
        img = create_frame(frame_num, scenario, total_frames, event_active)
        img.save(os.path.join(frames_path, f"frame_{frame_num:04d}.jpg"), quality=85)
        
        # Record event
        if event_active and frame_num % 20 == 0:  # Event every 20 frames
            events.append({
                "frame_number": frame_num,
                "event_type": scenario["event_type"],
                "severity": scenario["severity"],
                "ego_speed_mps": scenario["ego_speed_mps"] + random.uniform(-1, 1),
                "road_type": scenario["road_type"],
                "weather": scenario["weather"],
                "lead_distance_m": scenario["lead_distance_m"] + random.uniform(-2, 2),
                "cut_in_flag": scenario["cut_in_flag"]
            })
    
    # Create metadata
    metadata = {
        "name": scenario["name"],
        "description": scenario["description"],
        "total_frames": total_frames,
        "fps": 10,
        "duration_seconds": total_frames / 10,
        "upload_date": datetime.now().isoformat(),
        "events": events[:scenario["num_events"]]  # Limit number of events
    }
    
    with open(os.path.join(dataset_path, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)
    
    # Create telemetry.csv with exact required fields
    telemetry_path = os.path.join(dataset_path, "telemetry.csv")
    with open(telemetry_path, "w") as f:
        f.write("frame_id,timestamp,ego_speed_mps,ego_yaw,road_type,weather,lead_distance_m,cut_in_flag,pedestrian_flag,brake_flag\n")
        for i in range(total_frames):
            frame_id = f"frame_{i:06d}"
            timestamp = round(i / 10.0, 1)  # 10 fps
            speed = scenario["ego_speed_mps"] + random.uniform(-0.5, 0.5)
            ego_yaw = 0.0  # Straight driving
            road_type = scenario["road_type"]
            weather = scenario["weather"]
            lead_distance = scenario["lead_distance_m"] + random.uniform(-2, 2)
            
            # Determine flags based on event type and frame range
            event_active = scenario["frame_range"][0] <= i <= scenario["frame_range"][1]
            cut_in_flag = 1 if (event_active and scenario["event_type"] == "cut_in") else 0
            pedestrian_flag = 1 if (event_active and scenario["event_type"] == "pedestrian") else 0
            brake_flag = 1 if (event_active and scenario["event_type"] == "emergency_brake") else 0
            
            f.write(f"{frame_id},{timestamp},{speed:.2f},{ego_yaw},{road_type},{weather},{lead_distance:.1f},{cut_in_flag},{pedestrian_flag},{brake_flag}\n")
    
    print(f"✅ Generated dataset: {dataset_name}")
    print(f"   - {total_frames} frames")
    print(f"   - {len(metadata['events'])} events")
    print(f"   - Path: {dataset_path}")
    
    # Create ZIP file
    zip_path = f"{dataset_path}.zip"
    print(f"📦 Creating ZIP file...")
    shutil.make_archive(dataset_path, 'zip', dataset_path)
    print(f"✅ ZIP created: {os.path.basename(zip_path)}")
    
    return dataset_path, zip_path


if __name__ == "__main__":
    # Get the script directory and go up one level
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    output_dir = os.path.join(project_root, "backend", "storage", "datasets")
    os.makedirs(output_dir, exist_ok=True)
    
    print("🚗 Generating Realistic Autonomous Driving Datasets\n")
    
    # Generate all scenarios
    zip_files = []
    for scenario in SCENARIOS:
        dataset_path, zip_path = generate_dataset(output_dir, scenario)
        zip_files.append(zip_path)
        print()
    
    print("🎉 All datasets generated successfully!")
    print(f"\n📦 ZIP Files Created:")
    for zip_file in zip_files:
        print(f"   - {os.path.basename(zip_file)}")
    print(f"\nTo use them:")
    print(f"1. Upload ZIP files via the UI at http://localhost:5173")
    print(f"2. ZIP files are in: {output_dir}")
    print(f"3. Or use the unzipped folders directly")
