# ImageNet Model Inference - Streamlit Application

A dockerized Streamlit application for performing inference on images using trained ImageNet models.

## 🚀 Features

- **Easy-to-use Interface**: Upload images and get predictions instantly
- **Flexible Model Loading**: Use pretrained models or load your custom trained models
- **Top-K Predictions**: View multiple predictions with confidence scores
- **Confidence Filtering**: Filter predictions by confidence threshold
- **Docker Support**: Fully containerized for easy deployment
- **GPU Support**: Automatically uses GPU if available

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

1. Place your trained model checkpoint in the `models/` directory
2. In the sidebar, enter the path to your model (e.g., `/app/models/my_model.pth`)
3. Upload an image for inference

**Note:** The model loader expects PyTorch checkpoint files (.pth or .pt) with one of these formats:
- Direct state dict: `torch.load('model.pth')`
- Dictionary with `'model_state_dict'` key
- Dictionary with `'state_dict'` key

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

The application expects PyTorch models trained on ImageNet (1000 classes). If you're using a custom model:

1. Ensure it outputs 1000 classes
2. Save it as a PyTorch checkpoint (.pth or .pt)
3. Place it in the `models/` directory
4. Update the model architecture in `utils/model_loader.py` if needed

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
