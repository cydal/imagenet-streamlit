# Sample Images Directory

This folder contains sample images that users can test with the ImageNet Vision AI app.

## Usage

Place sample images in this directory. The app will automatically detect and display them as example images that users can click to run predictions on.

## Supported Formats

- JPG / JPEG
- PNG
- WebP
- GIF

## Recommended Images

For best results, include diverse ImageNet categories:
- Animals (dogs, cats, birds, etc.)
- Vehicles (cars, planes, boats, etc.)
- Objects (furniture, tools, electronics, etc.)
- Food items
- Natural scenes

## Image Requirements

- **Size**: Any size (will be automatically resized to 224x224 for inference)
- **Format**: RGB images work best
- **Quality**: Clear, well-lit images produce better predictions

## Adding Images

```bash
# Copy images to this directory
cp /path/to/your/image.jpg images/

# Or download from URL
wget -P images/ https://example.com/sample-image.jpg
```

## Note

Image files are gitignored to keep the repository size small. Only the `.gitkeep` and `README.md` files are tracked.
