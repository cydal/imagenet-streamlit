#\!/bin/bash
# Final deployment steps for HF Spaces

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   HF Spaces Deployment - ImageNet Vision AI               ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Backup and replace files
echo "📦 Step 1: Preparing files..."
cp Dockerfile Dockerfile.local
cp README.md README.local.md
cp .streamlit/config.toml .streamlit/config.local.toml

cp Dockerfile.hf Dockerfile
cp README.HF.md README.md
cp .streamlit/config.hf.toml .streamlit/config.toml

echo "✅ Files prepared"
echo ""

# Step 2: Show what changed
echo "📝 Step 2: Changes summary..."
echo "   - Dockerfile: Port 8501 → 7860, User 1000, Downloads model"
echo "   - README.md: Added HF Spaces metadata"
echo "   - config.toml: Port 7860"
echo "   - Model: Downloads from Sijuade/resnett50-imagenet"
echo ""

# Step 3: Commit
echo "💾 Step 3: Committing changes..."
git add .
git commit -m "Deploy to HF Spaces with model from Sijuade/resnett50-imagenet" || echo "No changes to commit"
echo "✅ Changes committed"
echo ""

# Step 4: Instructions
echo "╔════════════════════════════════════════════════════════════╗"
echo "║   Next Steps                                               ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "1. Create HF Space:"
echo "   → Visit: https://huggingface.co/new-space"
echo "   → Name: imagenet-vision-ai"
echo "   → SDK: Docker"
echo "   → Owner: Sijuade"
echo ""
echo "2. Add remote and push:"
echo "   git remote add hf https://huggingface.co/spaces/Sijuade/imagenet-vision-ai"
echo "   git push hf main"
echo ""
echo "3. Monitor build:"
echo "   → Visit your Space"
echo "   → Click 'Open Logs'"
echo "   → Wait for 'Running on http://0.0.0.0:7860'"
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║   Your Space will be live at:                              ║"
echo "║   https://huggingface.co/spaces/Sijuade/imagenet-vision-ai ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Create restore script
cat > restore_local.sh << 'RESTORE'
#\!/bin/bash
echo "Restoring local development files..."
cp Dockerfile.local Dockerfile
cp README.local.md README.md
cp .streamlit/config.local.toml .streamlit/config.toml
echo "✅ Local files restored"
RESTORE

chmod +x restore_local.sh
echo "📝 Created restore_local.sh to revert changes"
echo ""
