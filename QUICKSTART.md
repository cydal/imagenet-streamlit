# Quick Start Guide - ImageNet Vision AI

## 🚀 Setup and Run in 5 Minutes

Experience the beautiful new UI with drag-and-drop, multiple image uploads, and stunning visualizations!

### 1. Build Docker Image
```bash
cd /home/ubuntu/streamlit-imagenet-app
docker-compose build
```

### 2. Run the Application
```bash
docker-compose up
```

### 3. Access the App
Open your browser and go to: **http://localhost:8501**

You'll see:
- 🎨 Beautiful gradient header "ImageNet Vision AI"
- 📤 Drag-and-drop upload area
- ⚙️ Configuration sidebar
- 🎯 Real-time inference with stunning prediction cards

---

## Using with Trained Models

### Copy Checkpoint from Training Directory
```bash
# If you have a trained checkpoint from /home/ubuntu/imagenet
cp /home/ubuntu/imagenet/checkpoints/resnet50-epoch=*.ckpt \
   /home/ubuntu/streamlit-imagenet-app/models/
```

### In the Streamlit App
1. Enter the checkpoint path in the sidebar: `/app/models/resnet50-epoch=89.ckpt`
2. **Drag and drop** multiple images or click to browse
3. Watch the beautiful predictions appear with:
   - 🥇 Medal badges for top 3 predictions
   - 📊 Color-coded confidence scores
   - ⚡ Real-time inference times
   - 💾 Batch export to JSON

### New UI Features
- **Multiple Image Upload**: Process several images at once
- **Drag & Drop**: Just drag images into the upload area
- **Beautiful Cards**: Each prediction in a styled card with hover effects
- **Stats Dashboard**: See upload count, device type, and settings at a glance
- **Gradient Design**: Modern purple gradient theme throughout
- **Responsive Layout**: Works great on desktop and mobile

---

## Command-Line Inference (No Docker)

### Install Dependencies Locally
```bash
cd /home/ubuntu/streamlit-imagenet-app
pip install -r requirements.txt
```

### Run Inference Script
```bash
# With pretrained model
python inference.py --image /path/to/image.jpg

# With trained checkpoint
python inference.py \
    --image /path/to/image.jpg \
    --checkpoint /home/ubuntu/imagenet/checkpoints/resnet50-epoch=89.ckpt \
    --top_k 5 \
    --verbose
```

### Run Streamlit Locally
```bash
streamlit run app.py
```

---

## Testing with Sample Images

### Download a test image
```bash
# Download a sample ImageNet image
wget https://upload.wikimedia.org/wikipedia/commons/3/3a/Cat03.jpg -O test_cat.jpg

# Run inference
python inference.py --image test_cat.jpg --top_k 5
```

---

## Docker Commands Cheat Sheet

```bash
# Build
docker-compose build

# Run (foreground)
docker-compose up

# Run (background)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Rebuild and run
docker-compose up --build

# Remove everything
docker-compose down -v
```

---

## Troubleshooting

### Port 8501 already in use
Edit `docker-compose.yml` and change the port:
```yaml
ports:
  - "8502:8501"  # Use 8502 instead
```

### Out of memory
Reduce batch size or use CPU-only mode by commenting out GPU sections in `docker-compose.yml`.

### Model not loading
- Check the checkpoint path is correct
- Ensure the checkpoint file exists in the `models/` directory
- Check Docker logs: `docker-compose logs -f`
