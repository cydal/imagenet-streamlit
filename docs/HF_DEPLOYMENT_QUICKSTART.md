# Hugging Face Spaces Deployment - Quick Start

## TL;DR

```bash
# 1. Prepare files
./prepare_hf_deployment.sh

# 2. Review changes
git diff

# 3. Handle model checkpoint (choose one):
#    Option A: Use pretrained (no changes needed)
#    Option B: Download during build (update Dockerfile)
#    Option C: Use Git LFS (see below)

# 4. Commit changes
git add .
git commit -m "Prepare for HF Spaces deployment"

# 5. Create Space at https://huggingface.co/new-space
#    - Name: imagenet-vision-ai
#    - SDK: Docker
#    - Visibility: Public/Private

# 6. Push to HF
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/imagenet-vision-ai
git push hf main

# 7. Monitor build at your Space URL
```

## Key Changes Summary

### Files Modified
| File | Change | Why |
|------|--------|-----|
| `Dockerfile` | Port 8501 → 7860, Add user 1000 | HF Spaces requirements |
| `README.md` | Add YAML frontmatter | HF Spaces metadata |
| `.streamlit/config.toml` | Port 7860 | Match HF Spaces port |
| `app.py` | Checkpoint path to relative | Container compatibility |

### Critical Requirements
✅ **Port 7860** - HF Spaces default  
✅ **User ID 1000** - Security requirement  
✅ **Proper permissions** - All files owned by user  
✅ **README metadata** - YAML frontmatter with `sdk: docker`  

## Model Checkpoint Options

### Option 1: Use Pretrained (Easiest)
No changes needed. App will use torchvision pretrained ResNet50.

**Pros:** Simple, no large files  
**Cons:** Lower accuracy (70% vs 76%)

### Option 2: Download During Build
Add to `Dockerfile` before CMD:

```dockerfile
# Download checkpoint from external URL
RUN wget -O /app/models/acc1=76.2260.ckpt \
    https://your-storage-url.com/acc1=76.2260.ckpt && \
    chown user:user /app/models/acc1=76.2260.ckpt
```

**Pros:** Clean git repo  
**Cons:** Needs external hosting

### Option 3: Git LFS
```bash
# Install and setup Git LFS
git lfs install
git lfs track "*.ckpt"
git add .gitattributes

# Add checkpoint
cp /home/ubuntu/imagenet/checkpoints/acc1=76.2260.ckpt models/
git add models/acc1=76.2260.ckpt
git commit -m "Add model checkpoint via LFS"
```

**Pros:** Checkpoint in repo  
**Cons:** Requires LFS, slower clone

### Option 4: Hugging Face Hub
```bash
# Upload to HF Hub first
huggingface-cli upload YOUR_USERNAME/imagenet-resnet50 \
    /home/ubuntu/imagenet/checkpoints/acc1=76.2260.ckpt

# Then add to Dockerfile:
RUN pip install huggingface-hub && \
    python -c "from huggingface_hub import hf_hub_download; \
    hf_hub_download(repo_id='YOUR_USERNAME/imagenet-resnet50', \
                    filename='acc1=76.2260.ckpt', \
                    local_dir='/app/models')"
```

**Pros:** Proper model hosting  
**Cons:** Requires HF Hub setup

## Testing Locally

```bash
# Build Docker image
docker build -t imagenet-hf -f Dockerfile .

# Run container
docker run -it -p 7860:7860 imagenet-hf

# Test in browser
open http://localhost:7860
```

## Troubleshooting

### Build Fails
```bash
# Check logs in HF Space
# Click "Open Logs" → "Build" tab
```

### Permission Errors
```bash
# Ensure all COPY commands use --chown=user:user
COPY --chown=user:user . /app
```

### Port Not Working
```bash
# Verify all configs use 7860:
# - Dockerfile: EXPOSE 7860
# - CMD: --server.port=7860
# - README.md: app_port: 7860
# - config.toml: port = 7860
```

### Model Not Loading
```bash
# Check if checkpoint exists in container
# Add to Dockerfile for debugging:
RUN ls -lh /app/models/
```

## Restore Local Setup

```bash
# Revert to local development setup
./restore_local.sh

# Or manually:
cp Dockerfile.local Dockerfile
cp README.local.md README.md
cp .streamlit/config.local.toml .streamlit/config.toml
```

## Resources

- 📚 [Full Deployment Guide](./HUGGINGFACE_DEPLOYMENT.md)
- 🐳 [HF Docker Spaces Docs](https://huggingface.co/docs/hub/spaces-sdks-docker)
- 💡 [Docker Space Examples](https://huggingface.co/docs/hub/spaces-sdks-docker-examples)
- 🚀 [Create New Space](https://huggingface.co/new-space)

## Support

If you encounter issues:
1. Check [HUGGINGFACE_DEPLOYMENT.md](./HUGGINGFACE_DEPLOYMENT.md) for detailed troubleshooting
2. Review HF Spaces logs (Build + Container tabs)
3. Test locally with Docker first
4. Check HF Spaces documentation

---

**Ready to deploy?** Run `./prepare_hf_deployment.sh` to get started! 🚀
