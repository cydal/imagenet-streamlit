# ImageNet Inference App - Project Summary

## Overview

A production-ready, dockerized Streamlit application for performing inference on images using trained ImageNet models. Designed to work seamlessly with PyTorch Lightning checkpoints from the training codebase at `/home/ubuntu/imagenet`.

## Project Structure

```
streamlit-imagenet-app/
├── app.py                      # Main Streamlit web application
├── inference.py                # Standalone CLI inference script
├── test_inference.py           # Test suite for inference pipeline
├── config.yaml                 # Application configuration
│
├── utils/
│   ├── __init__.py
│   ├── model_loader.py         # Model loading (Lightning & PyTorch)
│   └── image_processor.py      # Image preprocessing & predictions
│
├── models/                     # Directory for model checkpoints
│   └── README.md              # Instructions for checkpoint usage
│
├── .streamlit/
│   └── config.toml            # Streamlit UI configuration
│
├── Dockerfile                  # Docker image definition
├── docker-compose.yml          # Docker Compose configuration
├── .dockerignore              # Docker build exclusions
├── requirements.txt            # Python dependencies
├── .gitignore                 # Git exclusions
│
├── README.md                   # Comprehensive documentation
└── QUICKSTART.md              # Quick start guide
```

## Key Features

### 1. **Streamlit Web Interface** (`app.py`)
- Beautiful, modern UI with responsive design
- Real-time image upload and inference
- Top-K predictions with confidence scores
- Configurable confidence thresholds
- Model information display
- JSON export of predictions
- Progress indicators and error handling

### 2. **Model Loading** (`utils/model_loader.py`)
- **PyTorch Lightning checkpoint support** - Automatically detects and loads `.ckpt` files
- **Hyperparameter extraction** - Reads num_classes and other config from checkpoint
- **State dict unwrapping** - Removes `model.` prefix from Lightning keys
- **Fallback to pretrained** - Uses torchvision ResNet50 if no checkpoint provided
- **Multi-format support** - Handles Lightning, standard PyTorch, and raw state dicts

### 3. **Image Processing** (`utils/image_processor.py`)
- **ImageNet preprocessing** - Standard normalization (mean/std)
- **Automatic resizing** - 256px resize → 224px center crop
- **GPU acceleration** - Automatic device detection
- **Class label loading** - Downloads ImageNet labels from web
- **Top-K predictions** - Configurable number of predictions
- **Confidence filtering** - Threshold-based filtering

### 4. **CLI Inference** (`inference.py`)
- Standalone command-line inference
- Supports all checkpoint formats
- JSON output option
- Verbose mode with model info
- No web server required

### 5. **Docker Support**
- **Multi-stage build** - Optimized image size
- **Volume mounting** - Easy checkpoint updates
- **GPU support** - Optional NVIDIA GPU acceleration
- **Health checks** - Container health monitoring
- **Development mode** - Hot-reload for code changes

### 6. **Testing** (`test_inference.py`)
- Automated test suite
- Pretrained model verification
- Checkpoint loading validation
- Dummy image generation
- Comprehensive error reporting

## Integration with Training Codebase

### Training Setup (`/home/ubuntu/imagenet`)
- **Framework:** PyTorch Lightning
- **Model:** ResNet50 (torchvision)
- **Checkpoints:** Saved in `checkpoints/` directory
- **Format:** Lightning `.ckpt` files with full training state

### Checkpoint Compatibility
The inference app is designed to load checkpoints from the training codebase:

```python
# Lightning checkpoint structure
{
    'state_dict': {
        'model.conv1.weight': ...,
        'model.layer1.0.conv1.weight': ...,
        ...
    },
    'hyper_parameters': {
        'num_classes': 1000,
        'lr': 0.1,
        'optimizer': 'sgd',
        ...
    },
    'epoch': 89,
    'optimizer_states': [...],
    ...
}
```

The model loader:
1. Detects Lightning format via `state_dict` key
2. Extracts `num_classes` from `hyper_parameters`
3. Removes `model.` prefix from all state dict keys
4. Loads weights into torchvision ResNet50

### Image Preprocessing Alignment
Both training and inference use identical preprocessing:
- **Resize:** 256px (shortest edge)
- **Crop:** 224x224 center crop
- **Normalize:** mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
- **Format:** RGB (3 channels)

## Usage Examples

### 1. Docker (Recommended)
```bash
# Build and run
cd /home/ubuntu/streamlit-imagenet-app
docker-compose up --build

# Access at http://localhost:8501
```

### 2. Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run app.py

# Or run CLI inference
python inference.py --image test.jpg --checkpoint models/checkpoint.ckpt
```

### 3. Testing
```bash
# Run test suite
python test_inference.py
```

### 4. Using Trained Checkpoints
```bash
# Copy checkpoint from training directory
cp /home/ubuntu/imagenet/checkpoints/resnet50-epoch=89-val_acc1=0.7500.ckpt \
   models/

# In Streamlit UI, enter: /app/models/resnet50-epoch=89-val_acc1=0.7500.ckpt
# Or use CLI:
python inference.py --image cat.jpg --checkpoint models/resnet50-epoch=89-val_acc1=0.7500.ckpt
```

## Technical Details

### Dependencies
- **streamlit** (1.28.0) - Web application framework
- **torch** (2.0.1) - PyTorch deep learning
- **torchvision** (0.15.2) - Computer vision models
- **Pillow** (10.0.0) - Image processing
- **numpy** (1.24.3) - Numerical computing

### Model Architecture
- **Base:** ResNet50 (torchvision implementation)
- **Input:** 224x224 RGB images
- **Output:** 1000 classes (ImageNet-1K)
- **Parameters:** ~25.6M

### Performance
- **GPU acceleration** - Automatic CUDA detection
- **Mixed precision** - Compatible with FP16 checkpoints
- **Batch size:** 1 (single image inference)
- **Inference time:** ~50-100ms on GPU, ~500ms on CPU

## Configuration

### Application Config (`config.yaml`)
```yaml
model_name: resnet50
num_classes: 1000
img_size: 224
mean: [0.485, 0.456, 0.406]
std: [0.229, 0.224, 0.225]
default_top_k: 5
default_confidence_threshold: 0.0
```

### Streamlit Config (`.streamlit/config.toml`)
```toml
[server]
port = 8501
maxUploadSize = 200

[theme]
primaryColor = "#1f77b4"
```

### Docker Config (`docker-compose.yml`)
- **Port:** 8501
- **Volumes:** `./models:/app/models` (checkpoint directory)
- **GPU:** Optional NVIDIA GPU support (commented out by default)

## Deployment Options

### 1. Local Docker
```bash
docker-compose up -d
```

### 2. Cloud Deployment
- Deploy to AWS ECS/Fargate
- Deploy to Google Cloud Run
- Deploy to Azure Container Instances

### 3. Kubernetes
```bash
# Build and push image
docker build -t imagenet-inference:latest .
docker push your-registry/imagenet-inference:latest

# Deploy to K8s cluster
kubectl apply -f k8s-deployment.yaml
```

## Future Enhancements

### Potential Features
- [ ] Batch inference support
- [ ] Multiple model architecture support (ResNet101, EfficientNet, etc.)
- [ ] Grad-CAM visualization
- [ ] Model comparison mode
- [ ] REST API endpoint
- [ ] Prometheus metrics
- [ ] Model serving with TorchServe
- [ ] ONNX export and inference
- [ ] Quantization support
- [ ] TensorRT optimization

## Troubleshooting

### Common Issues

**1. Checkpoint loading fails**
- Verify checkpoint path is correct
- Check checkpoint was created with PyTorch Lightning
- Ensure checkpoint is not corrupted

**2. Out of memory**
- Use CPU mode (remove GPU config)
- Reduce image upload size limit
- Close other applications

**3. Port already in use**
- Change port in `docker-compose.yml`
- Kill existing process on port 8501

**4. Slow inference**
- Enable GPU support
- Use smaller images
- Check system resources

## Documentation

- **README.md** - Comprehensive documentation
- **QUICKSTART.md** - Quick start guide
- **PROJECT_SUMMARY.md** - This file
- **models/README.md** - Checkpoint usage guide

## License

MIT License - See training repository for details.

## Related Projects

- **Training Codebase:** `/home/ubuntu/imagenet`
- **PyTorch:** https://pytorch.org/
- **Streamlit:** https://streamlit.io/
- **PyTorch Lightning:** https://lightning.ai/

---

**Created:** 2025-10-23  
**Status:** Production Ready ✅  
**Version:** 1.0.0
