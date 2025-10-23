# ImageNet Vision AI - Streamlit Application

A beautiful, production-ready Streamlit application for performing inference on images using trained ImageNet models. Features stunning UI/UX with drag-and-drop, multiple image uploads, and real-time predictions.

## 🚀 Features

### 🎨 Beautiful User Interface
- **Gradient Design**: Modern purple gradient theme with smooth animations
- **Drag & Drop**: Intuitive drag-and-drop interface for image uploads
- **Multiple Images**: Upload and process multiple images simultaneously
- **Prediction Cards**: Stunning card-based design with medals (🥇🥈🥉) for top predictions
- **Color-Coded Confidence**: Visual indicators (green/orange/gray) based on confidence levels
- **Real-Time Stats**: Dashboard showing upload count, device, and settings

### 🔥 Core Functionality
- **Flexible Model Loading**: Use pretrained models or load your custom Lightning checkpoints
- **Batch Processing**: Process multiple images in one session
- **Top-K Predictions**: View 1-10 top predictions per image
- **Confidence Filtering**: Filter predictions by confidence threshold
- **Inference Metrics**: Display inference time for each image
- **Batch Export**: Download all predictions as JSON

### 🐳 Deployment
- **Docker Support**: Fully containerized for easy deployment
- **GPU Support**: Automatically uses GPU if available
- **Hot Reload**: Development mode with code hot-reloading

## 📁 Project Structure

```
streamlit-imagenet-app/
├── app.py                      # Main Streamlit application
├── utils/
│   ├── __init__.py
│   ├── model_loader.py         # Model loading utilities
│   └── image_processor.py      # Image preprocessing utilities
├── models/                     # Directory for model checkpoints
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose configuration
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🛠️ Installation

### Option 1: Using Docker (Recommended)

1. **Build the Docker image:**
   ```bash
   docker-compose build
   ```

2. **Run the application:**
   ```bash
   docker-compose up
   ```

3. **Access the application:**
   Open your browser and navigate to `http://localhost:8501`

### Option 2: Local Installation

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## 🎯 Usage

### Using Pretrained Models

By default, the application uses a pretrained ResNet50 model from torchvision. Simply:

1. Launch the application
2. Upload an image (JPG, JPEG, or PNG)
3. View predictions with confidence scores

### Using Custom Trained Models

This application is designed to work with models trained using the ImageNet training codebase at `/home/ubuntu/imagenet`.

#### Loading PyTorch Lightning Checkpoints

1. Place your trained checkpoint in the `models/` directory
2. In the sidebar, enter the path to your checkpoint (e.g., `/app/models/resnet50-epoch=89.ckpt`)
3. Upload an image for inference

**Example:**
```bash
# Copy checkpoint from training directory
cp /home/ubuntu/imagenet/checkpoints/resnet50-epoch=89-val_acc1=0.7500.ckpt \
   /home/ubuntu/streamlit-imagenet-app/models/
```

**Supported Checkpoint Formats:**
- **PyTorch Lightning checkpoints** (.ckpt) - Automatically detects and loads from Lightning format
- **Standard PyTorch checkpoints** (.pth, .pt) with `'model_state_dict'` key
- **Direct state dict** - Raw model weights

The model loader automatically:
- Detects PyTorch Lightning checkpoint format
- Extracts hyperparameters (num_classes, etc.)
- Removes the `model.` prefix from Lightning state dict keys
- Handles different checkpoint structures

### Configuration Options

- **Number of predictions**: Adjust the slider to show top 1-10 predictions
- **Confidence threshold**: Filter out predictions below a certain confidence level
- **Model path**: Specify a custom model checkpoint path

## 🐳 Docker Commands

### Build the image:
```bash
docker-compose build
```

### Run in detached mode:
```bash
docker-compose up -d
```

### View logs:
```bash
docker-compose logs -f
```

### Stop the application:
```bash
docker-compose down
```

### Rebuild and restart:
```bash
docker-compose up --build
```

## 🖥️ GPU Support

To enable GPU support in Docker:

1. Install [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)

2. Uncomment the GPU-related sections in `docker-compose.yml`:
   ```yaml
   deploy:
     resources:
       reservations:
         devices:
           - driver: nvidia
             count: 1
             capabilities: [gpu]
   ```

3. Rebuild and run:
   ```bash
   docker-compose up --build
   ```

## 📝 Model Format

### Training Integration

This application is designed to work seamlessly with the ImageNet training codebase:

**Training Repository:** `/home/ubuntu/imagenet`

The training uses:
- **Framework:** PyTorch Lightning
- **Architecture:** ResNet50 (torchvision)
- **Image Size:** 224x224
- **Normalization:** ImageNet standard (mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
- **Classes:** 1000 (ImageNet-1K)

### Checkpoint Structure

PyTorch Lightning checkpoints contain:
```python
{
    'state_dict': {...},           # Model weights with 'model.' prefix
    'hyper_parameters': {          # Training config
        'num_classes': 1000,
        'lr': 0.1,
        'optimizer': 'sgd',
        ...
    },
    'epoch': 89,
    'global_step': ...,
    ...
}
```

The inference app automatically handles this structure.

### Standalone Inference Script

For command-line inference without the web UI:

```bash
# Using trained checkpoint
python inference.py \
    --image /path/to/image.jpg \
    --checkpoint /home/ubuntu/imagenet/checkpoints/resnet50-epoch=89.ckpt \
    --top_k 5

# Using pretrained model
python inference.py --image /path/to/image.jpg

# Save results to JSON
python inference.py \
    --image /path/to/image.jpg \
    --checkpoint /path/to/checkpoint.ckpt \
    --output results.json \
    --verbose
```

## 🔧 Customization

### Changing the Model Architecture

Edit `utils/model_loader.py` to use a different architecture:

```python
# Example: Using ResNet101 instead of ResNet50
model = models.resnet101(pretrained=False)
```

### Adding Custom Class Labels

Edit `utils/image_processor.py` to load custom class labels:

```python
def load_class_labels(labels_path=None):
    # Add your custom labels loading logic
    pass
```

### Modifying the UI

Edit `app.py` to customize the Streamlit interface, add new features, or change the layout.

## 📊 Example Output

The application provides:
- Visual display of uploaded image
- Ranked predictions with class names
- Confidence scores as percentages and progress bars
- Downloadable JSON file with predictions

## 🐛 Troubleshooting

### Port already in use
If port 8501 is already in use, modify the port mapping in `docker-compose.yml`:
```yaml
ports:
  - "8502:8501"  # Change 8502 to any available port
```

### Out of memory errors
Reduce the image upload size limit in `.streamlit/config.toml`:
```toml
maxUploadSize = 50  # Reduce from 200MB
```

### Model loading errors
Ensure your model checkpoint is compatible with the architecture defined in `model_loader.py`.

## 📦 Dependencies

- **streamlit**: Web application framework
- **torch**: PyTorch deep learning framework
- **torchvision**: Computer vision models and utilities
- **Pillow**: Image processing library
- **numpy**: Numerical computing library

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [PyTorch](https://pytorch.org/)
- Pretrained models from [torchvision](https://pytorch.org/vision/stable/index.html)
# imagenet-streamlit
