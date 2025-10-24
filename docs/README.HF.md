---
title: ImageNet Vision AI
emoji: 🖼️
colorFrom: purple
colorTo: violet
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# ImageNet Vision AI 🖼️

A beautiful, production-ready Streamlit application for performing inference on images using a trained ImageNet ResNet50 model. Features stunning UI/UX with drag-and-drop, multiple image uploads, and real-time predictions.

## 🚀 Features

### 🎨 Beautiful User Interface
- **Gradient Design**: Modern purple gradient theme with smooth animations
- **Drag & Drop**: Intuitive drag-and-drop interface for image uploads
- **Multiple Images**: Upload and process multiple images simultaneously
- **Prediction Cards**: Stunning card-based design with medals (🥇🥈🥉) for top predictions
- **Color-Coded Confidence**: Visual indicators (green/orange/gray) based on confidence levels
- **Real-Time Stats**: Dashboard showing upload count, device, and settings
- **Sample Images**: Try pre-loaded sample images with one click

### 🔥 Core Functionality
- **ResNet50 Model**: Trained on ImageNet with 76.23% top-1 accuracy
- **1000 Classes**: Full ImageNet classification
- **Batch Processing**: Process multiple images in one session
- **Top-K Predictions**: View 1-10 top predictions per image
- **Confidence Filtering**: Filter predictions by confidence threshold
- **Inference Metrics**: Display inference time for each image
- **Batch Export**: Download all predictions as JSON

### 🎯 Model Details
- **Architecture**: ResNet50
- **Dataset**: ImageNet (1000 classes)
- **Accuracy**: 76.21% top-1 accuracy
- **Framework**: PyTorch + PyTorch Lightning
- **Input Size**: 224×224 RGB images
- **Model Hub**: [Sijuade/resnett50-imagenet](https://huggingface.co/Sijuade/resnett50-imagenet)

## 🎨 How to Use

1. **Upload Images**: Drag and drop images or click to browse
2. **Try Samples**: Click on sample images to see instant predictions
3. **Adjust Settings**: Use sidebar to configure top-K predictions and confidence threshold
4. **View Results**: See beautiful prediction cards with confidence scores
5. **Export**: Download all predictions as JSON

## 📊 Example Predictions

The model can classify:
- 🐕 Animals (dogs, cats, birds, fish, etc.)
- 🚗 Vehicles (cars, planes, boats, etc.)
- 🪑 Objects (furniture, electronics, tools, etc.)
- 🍎 Food (fruits, vegetables, dishes, etc.)
- 🌸 Nature (flowers, plants, landscapes, etc.)

## 🛠️ Technology Stack

- **Frontend**: Streamlit with custom CSS
- **Backend**: PyTorch + torchvision
- **Model**: ResNet50 (PyTorch Lightning checkpoint)
- **Deployment**: Docker on Hugging Face Spaces

## 📝 About

This application demonstrates state-of-the-art image classification using a ResNet50 model trained on the ImageNet dataset. The model achieves 76.21% top-1 accuracy across 1000 object categories.

### Features Highlights:
- ✨ Beautiful gradient UI with animations
- 🎯 Accurate predictions with confidence scores
- ⚡ Fast inference (< 100ms per image)
- 📱 Responsive design for mobile and desktop
- 🎨 Sample image gallery for quick testing

## 🔗 Links

- [GitHub Repository](https://github.com/cydal/imagenet-streamlit)
- [Model Training Code](https://github.com/cydal/ImageNet-Full-training)
- [Model Repository](https://huggingface.co/Sijuade/resnett50-imagenet)
- [Hugging Face Space](https://huggingface.co/spaces/Sijuade/imagenet-vision-ai)

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- ImageNet dataset creators
- PyTorch and Streamlit teams
- Hugging Face for hosting

---

Built with ❤️ using Streamlit & PyTorch
