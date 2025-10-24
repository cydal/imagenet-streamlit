# Hugging Face Spaces Deployment - Summary

## What We Learned from the HF Tutorial

Based on https://huggingface.co/docs/hub/spaces-sdks-docker-first-demo:

### 1. **README Metadata (Required)**
```yaml
---
sdk: docker
app_port: 7860
---
```

### 2. **User ID 1000 (Required)**
```dockerfile
RUN useradd -m -u 1000 user
USER user
```

### 3. **Port 7860 (Default)**
```dockerfile
EXPOSE 7860
CMD ["streamlit", "run", "app.py", "--server.port=7860"]
```

### 4. **Proper Permissions**
```dockerfile
COPY --chown=user:user . /app
```

### 5. **Environment Variables**
```dockerfile
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH
```

## Changes We Need to Make

### ✅ Files Created

1. **`Dockerfile.hf`** - HF Spaces compatible Dockerfile
   - User ID 1000
   - Port 7860
   - Proper permissions

2. **`README.HF.md`** - README with HF metadata
   - YAML frontmatter
   - Space description
   - Usage instructions

3. **`.streamlit/config.hf.toml`** - HF Spaces Streamlit config
   - Port 7860
   - Headless mode
   - CORS disabled

4. **`prepare_hf_deployment.sh`** - Automated preparation script
   - Backs up local files
   - Swaps in HF versions
   - Updates checkpoint path
   - Creates restore script

5. **`HUGGINGFACE_DEPLOYMENT.md`** - Comprehensive deployment guide
   - Detailed instructions
   - Troubleshooting
   - All deployment options

6. **`HF_DEPLOYMENT_QUICKSTART.md`** - Quick reference
   - TL;DR commands
   - Model checkpoint options
   - Common issues

### 📝 Files to Modify

1. **`Dockerfile`** → Replace with `Dockerfile.hf`
   - Change port 8501 → 7860
   - Add user 1000
   - Fix permissions

2. **`README.md`** → Add YAML frontmatter
   ```yaml
   ---
   title: ImageNet Vision AI
   emoji: 🖼️
   sdk: docker
   app_port: 7860
   ---
   ```

3. **`app.py`** → Update checkpoint path
   ```python
   # From: "/home/ubuntu/imagenet/checkpoints/acc1=76.2260.ckpt"
   # To:   "models/acc1=76.2260.ckpt"
   ```

4. **`.streamlit/config.toml`** → Update port
   ```toml
   [server]
   port = 7860
   ```

## Deployment Workflow

```
┌─────────────────────────────────────────────────────────┐
│ 1. Prepare Files                                        │
│    ./prepare_hf_deployment.sh                           │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 2. Handle Model Checkpoint                              │
│    Choose: Pretrained / Download / LFS / HF Hub        │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 3. Test Locally (Optional)                              │
│    docker build -t test . && docker run -p 7860:7860    │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 4. Create HF Space                                      │
│    https://huggingface.co/new-space                     │
│    SDK: Docker, Port: 7860                              │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 5. Push to HF                                           │
│    git remote add hf <space-url>                        │
│    git push hf main                                     │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 6. Monitor Build                                        │
│    Check logs in Space → "Open Logs"                   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 7. Test Live Space                                      │
│    Upload images, verify predictions                    │
└─────────────────────────────────────────────────────────┘
```

## Key Differences: Local vs HF Spaces

| Aspect | Local Development | HF Spaces |
|--------|------------------|-----------|
| **Port** | 8501 | 7860 |
| **User** | root | user (UID 1000) |
| **Checkpoint Path** | `/home/ubuntu/imagenet/...` | `models/...` |
| **README** | Standard markdown | YAML frontmatter required |
| **Config** | `config.toml` | `config.hf.toml` |
| **Dockerfile** | `Dockerfile` | `Dockerfile.hf` |

## Model Checkpoint Strategy

### Recommended: Download During Build

Add to `Dockerfile.hf` before CMD:

```dockerfile
# Download model checkpoint
RUN wget -O /app/models/acc1=76.2260.ckpt \
    https://your-storage.com/acc1=76.2260.ckpt && \
    chown user:user /app/models/acc1=76.2260.ckpt
```

**Why?**
- ✅ Keeps git repo small
- ✅ Fast clone times
- ✅ Easy to update model
- ✅ No LFS complexity

**Alternatives:**
- Use pretrained model (lower accuracy)
- Git LFS (requires setup)
- HF Hub (proper ML hosting)

## Quick Commands

```bash
# Prepare for deployment
./prepare_hf_deployment.sh

# Test locally
docker build -t imagenet-hf .
docker run -it -p 7860:7860 imagenet-hf

# Deploy to HF
git remote add hf https://huggingface.co/spaces/USERNAME/imagenet-vision-ai
git add .
git commit -m "Deploy to HF Spaces"
git push hf main

# Restore local setup
./restore_local.sh
```

## Checklist Before Deployment

- [ ] Run `prepare_hf_deployment.sh`
- [ ] Choose model checkpoint strategy
- [ ] Update README with your HF username
- [ ] Test Docker build locally
- [ ] Create HF Space (SDK: Docker)
- [ ] Add HF remote
- [ ] Push to HF
- [ ] Monitor build logs
- [ ] Test live Space
- [ ] Update Space description/card

## Expected Build Time

- **First build**: 5-10 minutes
  - Installing dependencies
  - Downloading model (if applicable)
  
- **Subsequent builds**: 2-3 minutes
  - Docker layer caching
  - Only changed layers rebuild

## Resource Requirements

### Free Tier (CPU)
- ✅ Sufficient for inference
- ⚠️ Slower inference (~200-500ms)
- ⚠️ May timeout on first load

### GPU Tier (Paid)
- ✅ Fast inference (~50-100ms)
- ✅ Better user experience
- 💰 Costs apply

## Post-Deployment

### Monitor
- Check Space logs regularly
- Monitor usage/traffic
- Watch for errors

### Optimize
- Add caching for model loading
- Optimize Docker image size
- Consider GPU upgrade

### Maintain
- Update model as needed
- Keep dependencies current
- Respond to user feedback

## Support Resources

1. **Documentation**
   - [HUGGINGFACE_DEPLOYMENT.md](./HUGGINGFACE_DEPLOYMENT.md) - Full guide
   - [HF_DEPLOYMENT_QUICKSTART.md](./HF_DEPLOYMENT_QUICKSTART.md) - Quick ref

2. **HF Resources**
   - [Docker Spaces Docs](https://huggingface.co/docs/hub/spaces-sdks-docker)
   - [Space Examples](https://huggingface.co/docs/hub/spaces-sdks-docker-examples)
   - [Community Forum](https://discuss.huggingface.co/)

3. **Debugging**
   - Space logs (Build + Container tabs)
   - Local Docker testing
   - Dev Mode (VSCode/SSH access)

## Next Steps

1. **Review** the deployment guides
2. **Run** `./prepare_hf_deployment.sh`
3. **Choose** model checkpoint strategy
4. **Test** locally with Docker
5. **Deploy** to HF Spaces
6. **Share** your Space! 🎉

---

**Ready to deploy?** Start with `./prepare_hf_deployment.sh` 🚀
