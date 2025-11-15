"""
Convert nuScenes dataset to AutoLab format.

Requirements:
    pip install nuscenes-devkit

Usage:
    python scripts/convert_nuscenes.py --nuscenes-path /path/to/nuscenes --output backend/storage/datasets
"""

import os
import json
import shutil
import argparse
from pathlib import Path
import csv

try:
    from nuscenes.nuscenes import NuScenes
    from nuscenes.utils.data_classes import Box
    NUSCENES_AVAILABLE = True
except ImportError:
    NUSCENES_AVAILABLE = False
    print("⚠️  nuscenes-devkit not installed. Install with: pip install nuscenes-devkit")


def detect_events(sample_data, annotations):
    """Detect events from nuScenes annotations."""
    events = []
    
    # Check for pedestrians
    pedestrians = [ann for ann in annotations if 'pedestrian' in ann['category_name'].lower()]
    if pedestrians:
        events.append({
            'type': 'pedestrian',
            'severity': 'high' if len(pedestrians) > 2 else 'medium',
            'count': len(pedestrians)
        })
    
    # Check for vehicles cutting in (close proximity + lateral movement)
    vehicles = [ann for ann in annotations if 'vehicle' in ann['category_name'].lower()]
    close_vehicles = [v for v in vehicles if v.get('distance', 100) < 20]
    if close_vehicles:
        events.append({
            'type': 'cut_in',
            'severity': 'medium',
            'count': len(close_vehicles)
        })
    
    return events


def convert_scene(nusc, scene, output_dir):
    """Convert a single nuScenes scene to AutoLab format."""
    scene_name = scene['name']
    scene_token = scene['token']
    
    print(f"\n📦 Converting scene: {scene_name}")
    
    # Create output directory
    dataset_path = os.path.join(output_dir, f"nuScenes_{scene_name}")
    frames_path = os.path.join(dataset_path, "frames")
    os.makedirs(frames_path, exist_ok=True)
    
    # Get first sample
    sample_token = scene['first_sample_token']
    
    telemetry_data = []
    events = []
    frame_count = 0
    
    while sample_token:
        sample = nusc.get('sample', sample_token)
        
        # Get camera data (front camera)
        cam_front_data = nusc.get('sample_data', sample['data']['CAM_FRONT'])
        
        # Copy image to frames folder
        src_image = os.path.join(nusc.dataroot, cam_front_data['filename'])
        dst_image = os.path.join(frames_path, f"frame_{frame_count:06d}.jpg")
        
        if os.path.exists(src_image):
            shutil.copy2(src_image, dst_image)
        
        # Get ego pose
        ego_pose = nusc.get('ego_pose', cam_front_data['ego_pose_token'])
        
        # Get annotations
        annotations = [nusc.get('sample_annotation', token) for token in sample['anns']]
        
        # Calculate speed (simplified - from translation change)
        speed_mps = 10.0  # Default, would need to calculate from pose changes
        
        # Detect road type and weather (simplified)
        road_type = "urban"  # nuScenes is mostly urban
        weather = "clear"  # Would need to parse from scene description
        
        # Detect events
        frame_events = detect_events(cam_front_data, annotations)
        
        # Determine flags
        pedestrian_flag = 1 if any(e['type'] == 'pedestrian' for e in frame_events) else 0
        cut_in_flag = 1 if any(e['type'] == 'cut_in' for e in frame_events) else 0
        brake_flag = 0  # Would need CAN bus data
        
        # Add to telemetry
        telemetry_data.append({
            'frame_id': f"frame_{frame_count:06d}",
            'timestamp': round(frame_count * 0.5, 1),  # nuScenes is ~2Hz
            'ego_speed_mps': speed_mps,
            'ego_yaw': 0.0,
            'road_type': road_type,
            'weather': weather,
            'lead_distance_m': 30.0,  # Would need to calculate from annotations
            'cut_in_flag': cut_in_flag,
            'pedestrian_flag': pedestrian_flag,
            'brake_flag': brake_flag
        })
        
        # Record events
        if frame_events and frame_count % 10 == 0:  # Sample events
            for event in frame_events:
                events.append({
                    'frame_number': frame_count,
                    'event_type': event['type'],
                    'severity': event['severity'],
                    'ego_speed_mps': speed_mps,
                    'road_type': road_type,
                    'weather': weather,
                    'lead_distance_m': 30.0,
                    'cut_in_flag': cut_in_flag
                })
        
        frame_count += 1
        sample_token = sample['next']
    
    # Write telemetry.csv
    telemetry_path = os.path.join(dataset_path, 'telemetry.csv')
    with open(telemetry_path, 'w', newline='') as f:
        if telemetry_data:
            writer = csv.DictWriter(f, fieldnames=telemetry_data[0].keys())
            writer.writeheader()
            writer.writerows(telemetry_data)
    
    # Write metadata.json
    metadata = {
        'name': f"nuScenes - {scene_name}",
        'description': scene.get('description', 'nuScenes urban driving scene'),
        'total_frames': frame_count,
        'fps': 2,  # nuScenes is ~2Hz
        'duration_seconds': frame_count * 0.5,
        'source': 'nuScenes',
        'scene_token': scene_token,
        'events': events[:5]  # Limit to 5 events
    }
    
    with open(os.path.join(dataset_path, 'metadata.json'), 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✅ Converted {frame_count} frames")
    print(f"   Events detected: {len(events)}")
    print(f"   Output: {dataset_path}")
    
    # Create ZIP
    print(f"📦 Creating ZIP file...")
    shutil.make_archive(dataset_path, 'zip', dataset_path)
    print(f"✅ ZIP created: {os.path.basename(dataset_path)}.zip")
    
    return dataset_path


def main():
    parser = argparse.ArgumentParser(description='Convert nuScenes to AutoLab format')
    parser.add_argument('--nuscenes-path', required=True, help='Path to nuScenes dataset')
    parser.add_argument('--output', default='backend/storage/datasets', help='Output directory')
    parser.add_argument('--version', default='v1.0-mini', help='nuScenes version (v1.0-mini, v1.0-trainval)')
    parser.add_argument('--max-scenes', type=int, default=5, help='Maximum number of scenes to convert')
    
    args = parser.parse_args()
    
    if not NUSCENES_AVAILABLE:
        print("\n❌ Error: nuscenes-devkit not installed")
        print("\nInstall with:")
        print("   pip install nuscenes-devkit")
        return
    
    # Check if nuScenes path exists
    if not os.path.exists(args.nuscenes_path):
        print(f"\n❌ Error: nuScenes path not found: {args.nuscenes_path}")
        print("\nDownload nuScenes from: https://www.nuscenes.org/nuscenes#download")
        print("\nFor quick start, download 'v1.0-mini' (2.5 GB)")
        return
    
    print("🚗 nuScenes to AutoLab Converter\n")
    print(f"Input: {args.nuscenes_path}")
    print(f"Output: {args.output}")
    print(f"Version: {args.version}")
    print(f"Max scenes: {args.max_scenes}\n")
    
    # Load nuScenes
    print("📂 Loading nuScenes dataset...")
    try:
        nusc = NuScenes(version=args.version, dataroot=args.nuscenes_path, verbose=True)
    except Exception as e:
        print(f"\n❌ Error loading nuScenes: {e}")
        print("\nMake sure you have the correct version and path.")
        return
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    
    # Convert scenes
    converted = 0
    for scene in nusc.scene[:args.max_scenes]:
        try:
            convert_scene(nusc, scene, args.output)
            converted += 1
        except Exception as e:
            print(f"❌ Error converting scene {scene['name']}: {e}")
            continue
    
    print(f"\n🎉 Conversion complete!")
    print(f"   Converted {converted}/{args.max_scenes} scenes")
    print(f"   Output directory: {args.output}")
    print(f"\n✨ Ready to upload at http://localhost:5173")


if __name__ == '__main__':
    main()
