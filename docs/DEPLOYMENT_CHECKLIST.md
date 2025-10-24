# HF Spaces Deployment Checklist

## Pre-Deployment

### 1. Upload Model to HF Hub ✅

```bash
# Login to HF
huggingface-cli login

# Upload checkpoint
huggingface-cli upload cydal/imagenet-resnet50 \
    models/acc1=76.2100.ckpt \
    acc1=76.2100.ckpt
```

**Verify**: Visit https://huggingface.co/cydal/imagenet-resnet50

### 2. Update Files for HF Spaces

- [x] `app.py` - Checkpoint path updated to `models/acc1=76.2100.ckpt`
- [x] `Dockerfile.hf` - Downloads model from HF Hub
- [x] `README.HF.md` - Contains HF Spaces metadata
- [x] `.streamlit/config.hf.toml` - Port 7860 configuration

### 3. Test Model Loading Locally ✅

```bash
cd /home/ubuntu/streamlit-imagenet-app

# Test model loads correctly
conda run -n imagenet python -c "
from utils.model_loader import load_model
model = load_model('models/acc1=76.2100.ckpt')
print('✅ Model loads successfully!')
"
```

**Result**: Model loads with 85.59% confidence on test image ✅

## Deployment Steps

### Step 1: Prepare Repository

```bash
# Backup current files
cp Dockerfile Dockerfile.local
cp README.md README.local.md
cp .streamlit/config.toml .streamlit/config.local.toml

# Replace with HF versions
cp Dockerfile.hf Dockerfile
cp README.HF.md README.md
cp .streamlit/config.hf.toml .streamlit/config.toml

# Review changes
git diff
```

### Step 2: Commit Changes

```bash
git add .
git commit -m "Prepare for HF Spaces deployment with model from Hub"
```

### Step 3: Create HF Space

1. Go to: https://huggingface.co/new-space
2. Fill in details:
   - **Owner**: cydal
   - **Space name**: imagenet-vision-ai
   - **License**: MIT
   - **SDK**: Docker
   - **Visibility**: Public
3. Click "Create Space"

### Step 4: Push to HF Space

```bash
# Add HF Space as remote
git remote add hf https://huggingface.co/spaces/cydal/imagenet-vision-ai

# Push to HF
git push hf main
```

### Step 5: Monitor Build

1. Go to: https://huggingface.co/spaces/cydal/imagenet-vision-ai
2. Click "Open Logs" button
3. Watch "Build" tab:
   - Installing dependencies
   - Downloading model from Hub
   - Building Docker image
4. Watch "Container" tab:
   - Wait for "Running on http://0.0.0.0:7860"

**Expected build time**: 5-10 minutes (first build)

### Step 6: Test Live Space

1. Visit: https://huggingface.co/spaces/cydal/imagenet-vision-ai
2. Wait for app to load
3. Test features:
   - [ ] Upload an image
   - [ ] View predictions
   - [ ] Try sample images
   - [ ] Adjust settings (top-K, threshold)
   - [ ] Export to JSON
4. Verify:
   - [ ] Model loads correctly
   - [ ] Predictions are accurate
   - [ ] UI renders properly
   - [ ] No errors in logs

## Post-Deployment

### Update Space Card

Edit the Space README to add:
- Demo GIF/screenshots
- Usage examples
- Model performance details
- Links to model repository

### Share Your Space

- Tweet about it
- Share on LinkedIn
- Post in HF Discord
- Add to your portfolio

### Monitor Usage

- Check Space analytics
- Monitor error logs
- Respond to community feedback

## Verification Checklist

### Files
- [ ] `Dockerfile` uses port 7860
- [ ] `Dockerfile` creates user with UID 1000
- [ ] `Dockerfile` downloads model from HF Hub
- [ ] `README.md` has YAML frontmatter with `sdk: docker`
- [ ] `README.md` has `app_port: 7860`
- [ ] `.streamlit/config.toml` uses port 7860
- [ ] `app.py` uses relative checkpoint path

### Model
- [ ] Model uploaded to HF Hub
- [ ] Model accessible at `cydal/imagenet-resnet50`
- [ ] Checkpoint filename is `acc1=76.2100.ckpt`
- [ ] Model loads correctly in Dockerfile

### Testing
- [ ] Local model loading works
- [ ] Docker build succeeds locally (optional)
- [ ] HF Space build succeeds
- [ ] App runs on HF Spaces
- [ ] Predictions are accurate

## Rollback Plan

If deployment fails:

```bash
# Restore local files
cp Dockerfile.local Dockerfile
cp README.local.md README.md
cp .streamlit/config.local.toml .streamlit/config.toml

# Revert checkpoint path in app.py
# (if needed)

git add .
git commit -m "Revert to local setup"
```

## Troubleshooting

### Build Fails

**Check**: Build logs in HF Space
**Common issues**:
- Model download fails → Check HF Hub repo exists
- Permission errors → Verify `--chown=user:user` in Dockerfile
- Dependency errors → Check requirements.txt

### Model Not Loading

**Check**: Container logs
**Common issues**:
- Wrong checkpoint path
- Model file not downloaded
- Insufficient memory

### App Not Accessible

**Check**: Container logs for "Running on..."
**Common issues**:
- Wrong port in Dockerfile
- Streamlit not starting
- Container crashed

## Quick Commands

```bash
# Upload model
huggingface-cli upload cydal/imagenet-resnet50 models/acc1=76.2100.ckpt acc1=76.2100.ckpt

# Prepare deployment
cp Dockerfile.hf Dockerfile
cp README.HF.md README.md
cp .streamlit/config.hf.toml .streamlit/config.toml

# Deploy
git add .
git commit -m "Deploy to HF Spaces"
git remote add hf https://huggingface.co/spaces/cydal/imagenet-vision-ai
git push hf main

# Monitor
# Visit: https://huggingface.co/spaces/cydal/imagenet-vision-ai
# Click: "Open Logs"
```

## Success Criteria

✅ Model uploaded to HF Hub  
✅ Space builds successfully  
✅ App loads without errors  
✅ Predictions are accurate  
✅ UI is responsive  
✅ Sample images work  
✅ Export functionality works  

## Timeline

- **Model Upload**: 5-10 minutes (391MB file)
- **Space Creation**: 1 minute
- **First Build**: 5-10 minutes
- **Testing**: 5 minutes
- **Total**: ~20-30 minutes

---

**Ready to deploy?** Start with Step 1: Upload model to HF Hub! 🚀
