#\!/bin/bash
# Deploy to Hugging Face Spaces

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   Deploying to HF Spaces                                   ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Backup and prepare files
echo "📦 Step 1: Preparing files for HF Spaces..."
cp Dockerfile Dockerfile.local 2>/dev/null || true
cp README.md README.local.md 2>/dev/null || true
cp .streamlit/config.toml .streamlit/config.local.toml 2>/dev/null || true

cp Dockerfile.hf Dockerfile
cp .streamlit/config.hf.toml .streamlit/config.toml

# Add HF metadata to README
cat > README.md << 'README'
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

A beautiful Streamlit application for ImageNet image classification using ResNet50 (76.21% accuracy).

## 🚀 Features

- 🎨 Beautiful gradient UI with drag & drop
- 🖼️ Multiple image upload support
- 🎯 Top-K predictions with confidence scores
- 📊 Real-time inference metrics
- 💾 Export predictions to JSON
- 🎨 Sample image gallery

## 🎯 Model

- **Architecture**: ResNet50
- **Accuracy**: 76.21% top-1 on ImageNet
- **Classes**: 1000 ImageNet categories
- **Model Hub**: [Sijuade/resnett50-imagenet](https://huggingface.co/Sijuade/resnett50-imagenet)

## 🎨 How to Use

1. Upload images (drag & drop or click)
2. View top predictions with confidence scores
3. Try sample images for quick testing
4. Adjust settings in sidebar
5. Export results to JSON

Built with ❤️ using Streamlit & PyTorch
README

echo "✅ Files prepared"
echo ""

# Step 2: Commit changes
echo "💾 Step 2: Committing changes..."
git add Dockerfile README.md .streamlit/config.toml
git commit -m "Deploy to HF Spaces: Sijuade/imagenet-resnet50-inference" || echo "No changes to commit"
echo "✅ Changes committed"
echo ""

# Step 3: Add HF remote and push
echo "🚀 Step 3: Pushing to HF Spaces..."
git remote add hf https://huggingface.co/spaces/Sijuade/imagenet-resnet50-inference 2>/dev/null || \
    git remote set-url hf https://huggingface.co/spaces/Sijuade/imagenet-resnet50-inference

echo ""
echo "Ready to push\! Run:"
echo "  git push hf main"
echo ""
echo "Or if your branch is 'master':"
echo "  git push hf master:main"
echo ""

# Create restore script
cat > restore_local.sh << 'RESTORE'
#\!/bin/bash
echo "Restoring local development files..."
cp Dockerfile.local Dockerfile 2>/dev/null || true
cp README.local.md README.md 2>/dev/null || true
cp .streamlit/config.local.toml .streamlit/config.toml 2>/dev/null || true
echo "✅ Local files restored"
RESTORE

chmod +x restore_local.sh

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   After pushing, monitor your Space at:                    ║"
echo "║   https://huggingface.co/spaces/Sijuade/imagenet-resnet50-inference"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📝 To restore local setup later: ./restore_local.sh"
