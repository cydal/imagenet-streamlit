#\!/usr/bin/env python3
"""Download sample images from ImageNet sample repository"""

import os
import requests
from pathlib import Path

# Sample images to download (10 diverse images)
SAMPLE_IMAGES = [
    "n01440764_tench.JPEG",
    "n01443537_goldfish.JPEG", 
    "n01484850_great_white_shark.JPEG",
    "n01491361_tiger_shark.JPEG",
    "n01494475_hammerhead.JPEG",
    "n01496331_electric_ray.JPEG",
    "n01498041_stingray.JPEG",
    "n01514668_cock.JPEG",
    "n01514859_hen.JPEG",
    "n01518878_ostrich.JPEG"
]

BASE_URL = "https://raw.githubusercontent.com/EliSchwartz/imagenet-sample-images/master/"
OUTPUT_DIR = "images"

def download_sample_images():
    """Download sample images from GitHub"""
    
    # Create output directory
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    
    print(f"Downloading {len(SAMPLE_IMAGES)} sample images...")
    print(f"Output directory: {OUTPUT_DIR}/")
    print()
    
    success_count = 0
    for filename in SAMPLE_IMAGES:
        url = BASE_URL + filename
        output_path = os.path.join(OUTPUT_DIR, filename)
        
        # Skip if already exists
        if os.path.exists(output_path):
            print(f"✓ {filename} (already exists)")
            success_count += 1
            continue
        
        try:
            print(f"⬇ Downloading {filename}...", end=" ")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            file_size = os.path.getsize(output_path) / 1024  # KB
            print(f"✓ ({file_size:.1f} KB)")
            success_count += 1
            
        except Exception as e:
            print(f"✗ Failed: {e}")
    
    print()
    print(f"{'='*60}")
    print(f"Downloaded {success_count}/{len(SAMPLE_IMAGES)} images successfully")
    print(f"Location: {os.path.abspath(OUTPUT_DIR)}/")
    print(f"{'='*60}")

if __name__ == "__main__":
    download_sample_images()
