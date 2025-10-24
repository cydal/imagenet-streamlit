# Deploying to Hugging Face Spaces

## Overview

This guide explains how to deploy the ImageNet Vision AI app to Hugging Face Spaces using Docker.

## Key Requirements for HF Spaces

Based on the [HF Spaces Docker tutorial](https://huggingface.co/docs/hub/spaces-sdks-docker-first-demo), we need:

### 1. README.md Metadata
Add YAML frontmatter to README.md:
```yaml
---
title: ImageNet Vision AI
emoji: 🖼️
colorFrom: purple
colorTo: violet
sdk: docker
app_port: 7860
---
```

### 2. Dockerfile Changes
- **User ID 1000**: HF Spaces runs containers with user ID 1000
- **Port 7860**: Default HF Spaces port (can be changed via `app_port`)
- **Permissions**: Set proper ownership for user 1000
- **Working Directory**: `/app`

### 3. Model Checkpoint
- Cannot include 391MB checkpoint in git repo
- Options:
  1. Download from HF Hub during build
  2. Use HF Spaces secrets for model path
  3. Host checkpoint separately and download

## Changes Needed

### 1. Update README.md
Add HF Spaces metadata at the top:

```markdown
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

# ImageNet Vision AI
...rest of README...
```

### 2. Update Dockerfile

**Current Issues:**
- Port 8501 (Streamlit default) → Need 7860 (HF default)
- No user setup for UID 1000
- Missing proper permissions

**Required Changes:**

```dockerfile
# Read the doc: https://huggingface.co/docs/hub/spaces-sdks-docker
FROM python:3.9-slim

# Create user with UID 1000 (required for HF Spaces)
RUN useradd -m -u 1000 user

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install (with proper ownership)
COPY --chown=user:user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (with proper ownership)
COPY --chown=user:user . /app

# Create directories with proper permissions
RUN mkdir -p /app/models /app/images && \
    chown -R user:user /app

# Switch to user
USER user

# Set environment variables
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_PORT=7860 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Expose port 7860 (HF Spaces default)
EXPOSE 7860

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
```

### 3. Handle Model Checkpoint

**Option A: Download from Hugging Face Hub**

Add to Dockerfile before CMD:
```dockerfile
# Download model checkpoint from HF Hub
RUN python -c "from huggingface_hub import hf_hub_download; \
    hf_hub_download(repo_id='YOUR_USERNAME/imagenet-resnet50', \
                    filename='acc1=76.2260.ckpt', \
                    local_dir='/app/models')"
```

**Option B: Use Git LFS (if checkpoint is in repo)**

1. Install git-lfs:
```bash
git lfs install
git lfs track "*.ckpt"
git add .gitattributes
```

2. Add checkpoint:
```bash
git add models/acc1=76.2260.ckpt
git commit -m "Add model checkpoint"
```

**Option C: Download from External URL**

Add to Dockerfile:
```dockerfile
# Download model from external URL
RUN curl -L -o /app/models/acc1=76.2260.ckpt \
    https://your-storage-url.com/acc1=76.2260.ckpt
```

**Option D: Use Pretrained Model (Fallback)**

Modify `app.py` to use pretrained if checkpoint not found:
```python
checkpoint_path = "/app/models/acc1=76.2260.ckpt"
if not os.path.exists(checkpoint_path):
    checkpoint_path = None  # Will load pretrained ResNet50
```

### 4. Update .streamlit/config.toml

Create `.streamlit/config.toml` for HF Spaces:
```toml
[server]
port = 7860
address = "0.0.0.0"
headless = true
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
serverAddress = "0.0.0.0"
serverPort = 7860
```

### 5. Update app.py Checkpoint Path

Change from absolute path to relative:
```python
# Old (local development)
checkpoint_path = "/home/ubuntu/imagenet/checkpoints/acc1=76.2260.ckpt"

# New (HF Spaces compatible)
checkpoint_path = "models/acc1=76.2260.ckpt"
```

## Deployment Steps

### Step 1: Create HF Space

1. Go to https://huggingface.co/new-space
2. Choose a name: `imagenet-vision-ai`
3. Select **Docker** as SDK
4. Choose visibility (Public/Private)
5. Click "Create Space"

### Step 2: Prepare Repository

```bash
cd /home/ubuntu/streamlit-imagenet-app

# Update README with HF metadata
# (Add YAML frontmatter)

# Update Dockerfile for HF Spaces
# (Use the new Dockerfile above)

# Update checkpoint path in app.py
# (Change to relative path)

# Create .streamlit/config.toml
# (Add HF-specific config)

# Commit changes
git add .
git commit -m "Prepare for HF Spaces deployment"
```

### Step 3: Push to HF Space

```bash
# Add HF Space as remote
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/imagenet-vision-ai

# Push to HF Space
git push hf main
```

### Step 4: Handle Model Checkpoint

**If using external download:**
- Checkpoint will download during build
- First build will take longer

**If using HF Hub:**
- Upload checkpoint to HF Hub first
- Update Dockerfile to download from Hub

**If using Git LFS:**
- Enable Git LFS in Space settings
- Push checkpoint with git-lfs

### Step 5: Monitor Build

1. Go to your Space page
2. Click "Open Logs" button
3. Check "Build" tab for build progress
4. Check "Container" tab for runtime logs
5. Wait for "Running on http://0.0.0.0:7860"

### Step 6: Test

1. Visit your Space URL
2. Upload test images
3. Verify predictions work
4. Test sample images feature

## File Checklist

- [ ] `README.md` - Add HF metadata
- [ ] `Dockerfile` - Update for HF Spaces (user 1000, port 7860)
- [ ] `app.py` - Change checkpoint path to relative
- [ ] `.streamlit/config.toml` - Add HF-specific config
- [ ] `requirements.txt` - Verify all dependencies
- [ ] `.gitignore` - Ensure proper files ignored
- [ ] Model checkpoint - Choose deployment strategy

## Port Configuration

| Environment | Port | Configuration |
|-------------|------|---------------|
| Local Dev | 8501 | Streamlit default |
| Docker Local | 8501 | docker-compose.yml |
| HF Spaces | 7860 | README.md `app_port` |

## Environment Variables

HF Spaces automatically sets:
- `SPACE_ID` - Your space ID
- `SPACE_AUTHOR_NAME` - Your username
- `SPACE_REPO_NAME` - Space name

You can add custom secrets in Space settings.

## Troubleshooting

### Build Fails
- Check "Build" logs in Space
- Verify Dockerfile syntax
- Check requirements.txt dependencies

### Permission Errors
- Ensure user 1000 owns all files
- Check `--chown=user:user` in COPY commands
- Verify directory permissions

### Model Loading Fails
- Check checkpoint path is correct
- Verify checkpoint exists in container
- Check logs for loading errors

### Port Issues
- Verify port 7860 in all configs
- Check Streamlit runs on 0.0.0.0:7860
- Ensure `app_port: 7860` in README

### Out of Memory
- Model + dependencies may exceed free tier
- Consider:
  - Upgrading to GPU Space
  - Using smaller model
  - Optimizing dependencies

## Optimization Tips

### 1. Reduce Image Size
```dockerfile
# Use multi-stage build
FROM python:3.9-slim as builder
# Build dependencies
FROM python:3.9-slim
# Copy only necessary files
```

### 2. Cache Dependencies
```dockerfile
# Copy requirements first
COPY requirements.txt .
RUN pip install -r requirements.txt
# Then copy code (better caching)
COPY . .
```

### 3. Minimize Layers
```dockerfile
# Combine RUN commands
RUN apt-get update && \
    apt-get install -y pkg1 pkg2 && \
    rm -rf /var/lib/apt/lists/*
```

## GPU Support

To use GPU on HF Spaces:

1. Upgrade Space to GPU tier
2. Update Dockerfile:
```dockerfile
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04
# Install Python and dependencies
```

3. Update requirements.txt:
```
torch==2.0.1+cu118
torchvision==0.15.2+cu118
```

## Cost Considerations

- **Free Tier**: CPU-only, limited resources
- **GPU Tier**: Paid, better performance
- **Persistent Storage**: Consider for large models

## Example Spaces

Reference these Docker Spaces:
- [DockerTemplates/fastapi_t5](https://huggingface.co/spaces/DockerTemplates/fastapi_t5)
- [DockerTemplates/fastapi_dummy](https://huggingface.co/spaces/DockerTemplates/fastapi_dummy)

## Resources

- [HF Spaces Docker Guide](https://huggingface.co/docs/hub/spaces-sdks-docker)
- [Docker Space Examples](https://huggingface.co/docs/hub/spaces-sdks-docker-examples)
- [Dev Mode](https://huggingface.co/dev-mode-explorers)

---

**Next Steps**: Follow the deployment steps above to get your Space live!
