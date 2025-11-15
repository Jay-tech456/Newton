"""
Create ZIP files from existing datasets for easy upload.
"""
import os
import shutil

def create_zips():
    # Get absolute paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    datasets_dir = os.path.join(project_root, "backend", "storage", "datasets")
    output_dir = os.path.join(project_root, "demo_datasets")
    
    os.makedirs(output_dir, exist_ok=True)
    
    print("📦 Creating ZIP files from existing datasets...\n")
    
    # Find all dataset directories (only recent ones with telemetry.csv)
    datasets = []
    for item in os.listdir(datasets_dir):
        item_path = os.path.join(datasets_dir, item)
        if os.path.isdir(item_path) and item != "demos":
            # Check if it has frames AND telemetry.csv
            frames_path = os.path.join(item_path, "frames")
            telemetry_path = os.path.join(item_path, "telemetry.csv")
            if os.path.exists(frames_path) and os.path.exists(telemetry_path):
                # Only include datasets from today
                if "145632" in item or "145633" in item or "145635" in item or "145636" in item:
                    datasets.append((item, item_path))
    
    if not datasets:
        print("❌ No datasets found!")
        return
    
    zip_files = []
    for name, path in datasets:
        print(f"Creating ZIP for: {name}")
        zip_path = os.path.join(output_dir, name)
        shutil.make_archive(zip_path, 'zip', path)
        zip_files.append(f"{zip_path}.zip")
        print(f"✅ Created: {name}.zip\n")
    
    print(f"🎉 Created {len(zip_files)} ZIP files!")
    print(f"\n📁 Location: {os.path.abspath(output_dir)}")
    print(f"\n📦 Files:")
    for zf in zip_files:
        size_mb = os.path.getsize(zf) / (1024 * 1024)
        print(f"   - {os.path.basename(zf)} ({size_mb:.1f} MB)")
    
    print(f"\n✨ Ready to upload at http://localhost:5173")

if __name__ == "__main__":
    create_zips()
