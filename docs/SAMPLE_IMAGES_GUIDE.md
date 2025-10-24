# Sample Images Guide

## Overview

The `images/` folder contains sample images that users can test with the ImageNet Vision AI app. When no images are uploaded, the app displays these samples in a grid, allowing users to click and run predictions instantly.

## Features

### 🎨 Sample Image Gallery
- Displays all images from the `images/` folder in a 4-column grid
- Click "Predict" button on any sample to run inference
- Results shown in the same beautiful UI as uploaded images

### 🔒 Git Ignored
- Image files (`.jpg`, `.png`, `.webp`, etc.) are gitignored
- Keeps repository size small
- Only folder structure and README are tracked

## Adding Sample Images

### Method 1: Copy Local Files
```bash
# Copy images to the folder
cp /path/to/your/images/*.jpg images/

# Example: Copy from ImageNet validation set
cp /home/ubuntu/imagenet/val/n01440764/*.JPEG images/
```

### Method 2: Download from URL
```bash
# Download a single image
wget -P images/ https://example.com/dog.jpg

# Download multiple images
for url in url1 url2 url3; do
    wget -P images/ $url
done
```

### Method 3: Use ImageNet Samples
```bash
# Copy diverse samples from your ImageNet dataset
# Pick one image from different classes
cp /home/ubuntu/imagenet/val/n01440764/ILSVRC2012_val_00000293.JPEG images/fish.jpg
cp /home/ubuntu/imagenet/val/n02084071/ILSVRC2012_val_00000247.JPEG images/dog.jpg
cp /home/ubuntu/imagenet/val/n02121808/ILSVRC2012_val_00000312.JPEG images/cat.jpg
```

## Recommended Sample Set

For a diverse demo, include images from these categories:

### Animals
- Dog (Golden Retriever, Labrador)
- Cat (Tabby, Persian)
- Bird (Eagle, Parrot)
- Fish (Goldfish, Shark)
- Wild animals (Lion, Elephant, Tiger)

### Vehicles
- Car (Sports car, Sedan)
- Airplane
- Boat/Ship
- Bicycle
- Motorcycle

### Objects
- Furniture (Chair, Table)
- Electronics (Laptop, Phone)
- Kitchen items (Coffee mug, Toaster)
- Sports equipment (Basketball, Tennis racket)

### Food
- Fruits (Apple, Banana, Orange)
- Vegetables (Broccoli, Carrot)
- Prepared food (Pizza, Burger)

### Nature
- Flowers (Rose, Sunflower)
- Landscapes
- Trees

## Image Requirements

- **Format**: JPG, JPEG, PNG, WebP, GIF
- **Size**: Any size (automatically resized to 224×224)
- **Quality**: Clear, well-lit images work best
- **Content**: Single main subject preferred

## File Naming

Use descriptive names for better UX:
```
✅ Good:
- golden_retriever.jpg
- sports_car.jpg
- coffee_mug.png

❌ Avoid:
- IMG_1234.jpg
- image.png
- photo.jpg
```

## Testing Your Samples

1. Add images to the `images/` folder
2. Restart the Streamlit app (or it will auto-reload)
3. Navigate to the app without uploading files
4. Scroll down to see "🎨 Try Sample Images"
5. Click "Predict" on any sample

## Folder Structure

```
images/
├── .gitkeep              # Keeps folder in git
├── README.md             # This guide (tracked)
├── dog.jpg               # Sample image (gitignored)
├── cat.jpg               # Sample image (gitignored)
├── car.jpg               # Sample image (gitignored)
└── ...                   # More samples (gitignored)
```

## App Behavior

### With Sample Images
- Empty state shows upload area
- Below that, displays "🎨 Try Sample Images" section
- 4-column grid of clickable sample images
- Click "Predict" to run inference on that sample

### Without Sample Images
- Only shows upload area
- No sample section displayed
- Users must upload their own images

## Performance Tips

- **Limit quantity**: 8-12 samples is ideal
- **Optimize size**: Resize large images before adding
- **Diverse categories**: Show variety of ImageNet classes
- **High quality**: Use clear, professional images

## Example Script to Add Samples

```bash
#!/bin/bash
# add_samples.sh - Add diverse ImageNet samples

IMAGES_DIR="images"
VAL_DIR="/home/ubuntu/imagenet/val"

# Create array of class folders and sample files
declare -A samples=(
    ["n02084071"]="dog.jpg"           # Dog
    ["n02121808"]="cat.jpg"           # Cat
    ["n01440764"]="fish.jpg"          # Fish
    ["n02930766"]="car.jpg"           # Car
    ["n04389033"]="table.jpg"         # Table
    ["n03793489"]="mouse.jpg"         # Computer mouse
    ["n07753592"]="banana.jpg"        # Banana
    ["n02690373"]="airplane.jpg"      # Airplane
)

# Copy samples
for class_id in "${!samples[@]}"; do
    output_name="${samples[$class_id]}"
    # Get first image from that class
    first_image=$(ls "$VAL_DIR/$class_id"/*.JPEG 2>/dev/null | head -1)
    
    if [ -f "$first_image" ]; then
        cp "$first_image" "$IMAGES_DIR/$output_name"
        echo "✓ Added $output_name"
    else
        echo "✗ Class $class_id not found"
    fi
done

echo "Done! Added ${#samples[@]} sample images."
```

## Troubleshooting

### Images Not Showing
- Check file extensions are supported (jpg, png, webp, gif)
- Verify files are in `images/` folder (not subfolders)
- Restart Streamlit app

### Images Show But Can't Predict
- Check image files are valid and not corrupted
- Ensure images can be opened by PIL/Pillow
- Check app logs for errors

### Too Many Images
- Keep to 8-12 samples for best UX
- Remove unused samples
- Consider creating categories if you need more

## Best Practices

1. **Curate Quality**: Only include clear, representative images
2. **Diverse Classes**: Show variety of ImageNet categories
3. **Descriptive Names**: Use meaningful filenames
4. **Test Predictions**: Verify samples give good predictions
5. **Update Regularly**: Refresh samples periodically

---

**Note**: Sample images are for demonstration purposes only. Ensure you have rights to use any images you add.
