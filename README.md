---
title: ImageNet Vision AI
emoji: 🖼️
colorFrom: purple
colorTo: pink
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# ImageNet Vision AI 🖼️

A beautiful, production-ready Streamlit application for ImageNet image classification using a custom-trained ResNet50 model achieving **76.21% top-1 accuracy**.

## ✨ Live Demo

Try it now: [ImageNet Vision AI on Hugging Face Spaces](https://huggingface.co/spaces/Sijuade/imagenet-resnet50-inference)

## 🚀 Features

### 🎨 Beautiful User Interface
- **Modern Design**: Purple gradient theme with smooth animations
- **Drag & Drop**: Intuitive interface for image uploads
- **Multiple Images**: Upload and process multiple images simultaneously
- **Prediction Cards**: Stunning card-based design with medals (🥇🥈🥉) for top predictions
- **Color-Coded Confidence**: Visual indicators (green/orange/gray) based on confidence levels
- **Sample Gallery**: 4 pre-loaded ImageNet sample images for quick testing

### 🔥 Core Functionality
- **Top-K Predictions**: View 1-10 top predictions per image
- **Confidence Filtering**: Filter predictions by confidence threshold
- **Inference Metrics**: Display inference time for each image
- **Batch Processing**: Process multiple images in one session
- **Batch Export**: Download all predictions as JSON

## 🎯 Model Details

- **Architecture**: ResNet50 (PyTorch)
- **Training**: Custom training on full ImageNet-1K dataset
- **Accuracy**: 76.21% top-1 accuracy
- **Classes**: 1000 ImageNet categories
- **Framework**: PyTorch Lightning with mixed precision (FP16)
- **Optimizer**: LAMB with cosine learning rate schedule
- **Augmentation**: RandAugment, Mixup (0.2), CutMix (1.0), Random Erasing (0.25)
- **Training Details**: 300 epochs, 8 GPUs (DDP), batch size 256

### 📦 Model Repository
- **Checkpoint**: [Sijuade/resnett50-imagenet](https://huggingface.co/Sijuade/resnett50-imagenet)
- **Training Code**: [ImageNet-Full-training](https://github.com/cydal/ImageNet-Full-training)

## 🎨 How to Use

1. **Upload Images**: Drag and drop images or click to browse (JPG, JPEG, PNG, WebP)
2. **Try Samples**: Click on any of the 4 sample images to see instant predictions
3. **Adjust Settings**: Use sidebar to configure:
   - Top-K predictions (1-10)
   - Confidence threshold (0-100%)
   - Show/hide inference time
   - Show/hide model info
4. **View Results**: See beautiful prediction cards with:
   - Class names
   - Confidence scores
   - Visual progress bars
   - Medal indicators for top 3
5. **Export**: Download all predictions as JSON

## 🛠️ Technology Stack

- **Frontend**: Streamlit with custom CSS
- **Backend**: PyTorch + torchvision
- **Model**: ResNet50 (PyTorch Lightning checkpoint)
- **Deployment**: Docker on Hugging Face Spaces
- **Sample Images**: From [imagenet-sample-images](https://github.com/EliSchwartz/imagenet-sample-images)

## 🐳 Docker Deployment

This app is deployed using Docker on Hugging Face Spaces. Key features:

- **Automatic Model Download**: Downloads 391MB checkpoint from Hugging Face Hub during build
- **Sample Images**: Downloads 10 sample images from GitHub during build (limited to 4 in UI)
- **User Permissions**: Runs as user ID 1000 (HF Spaces requirement)
- **Port**: Exposes port 7860 (HF Spaces default)

### Dockerfile Highlights

```dockerfile
# Download model from HF Hub
RUN python -c "from huggingface_hub import hf_hub_download; \
    hf_hub_download(repo_id='Sijuade/resnett50-imagenet', \
                    filename='acc1=76.2100.ckpt', \
                    local_dir='/app/models')"

# Download sample images from GitHub
RUN python -c "import os, requests; \
    samples = ['n01440764_tench.JPEG', 'n01443537_goldfish.JPEG', ...]; \
    [open(os.path.join('/app/images', f), 'wb').write(requests.get(base_url + f).content) for f in samples]"
```

## 📊 Example Predictions

The model can classify:
- 🐕 **Animals**: Dogs, cats, birds, fish, reptiles, insects
- 🚗 **Vehicles**: Cars, planes, boats, trains, bicycles
- 🪑 **Objects**: Furniture, electronics, tools, instruments
- 🍎 **Food**: Fruits, vegetables, dishes, beverages
- 🌸 **Nature**: Flowers, plants, landscapes, natural formations

## 🔧 Local Development

### Using Docker

```bash
# Clone the repository
git clone https://github.com/cydal/imagenet-streamlit.git
cd imagenet-streamlit

# Build and run
docker build -t imagenet-vision-ai .
docker run -p 7860:7860 imagenet-vision-ai
```

### Using Python

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 📝 Training Your Own Model

Want to train your own ImageNet model? Check out the training repository:

**[ImageNet-Full-training](https://github.com/cydal/ImageNet-Full-training)**

Features:
- Full ImageNet-1K training pipeline
- PyTorch Lightning implementation
- Multi-GPU (DDP) support
- Mixed precision (FP16) training
- Advanced augmentation techniques
- Cosine learning rate scheduling
- LAMB optimizer
- Model compilation with `torch.compile()`

## 🔗 Links

- **Live App**: [Hugging Face Space](https://huggingface.co/spaces/Sijuade/imagenet-resnet50-inference)
- **Model**: [Sijuade/resnett50-imagenet](https://huggingface.co/Sijuade/resnett50-imagenet)
- **Training Code**: [ImageNet-Full-training](https://github.com/cydal/ImageNet-Full-training)
- **App Code**: [imagenet-streamlit](https://github.com/cydal/imagenet-streamlit)

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- **ImageNet Dataset**: [ImageNet Large Scale Visual Recognition Challenge](https://www.image-net.org/)
- **PyTorch**: Deep learning framework
- **Streamlit**: Web application framework
- **Hugging Face**: Model hosting and Spaces platform
- **Sample Images**: [EliSchwartz/imagenet-sample-images](https://github.com/EliSchwartz/imagenet-sample-images)

---

Built with ❤️ using Streamlit & PyTorch | **76.21% Top-1 Accuracy** on ImageNet-1K
