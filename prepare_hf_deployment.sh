#!/bin/bash
# Script to prepare the repository for Hugging Face Spaces deployment

set -e

echo "========================================="
echo "Preparing for Hugging Face Spaces Deploy"
echo "========================================="
echo ""

# 1. Backup current files
echo "📦 Creating backups..."
cp Dockerfile Dockerfile.local
cp README.md README.local.md
cp .streamlit/config.toml .streamlit/config.local.toml
echo "✅ Backups created"
echo ""

# 2. Replace with HF versions
echo "🔄 Replacing files with HF versions..."
cp Dockerfile.hf Dockerfile
cp README.HF.md README.md
cp .streamlit/config.hf.toml .streamlit/config.toml
echo "✅ Files replaced"
echo ""

# 3. Update app.py checkpoint path
echo "📝 Updating checkpoint path in app.py..."
sed -i 's|checkpoint_path = "/home/ubuntu/imagenet/checkpoints/acc1=76.2260.ckpt"|checkpoint_path = "models/acc1=76.2260.ckpt"|g' app.py
echo "✅ Checkpoint path updated"
echo ""

# 4. Check for model checkpoint
echo "🔍 Checking for model checkpoint..."
if [ -f "models/acc1=76.2260.ckpt" ]; then
    echo "✅ Model checkpoint found"
    echo "⚠️  WARNING: Checkpoint is 391MB - too large for git"
    echo "   Options:"
    echo "   1. Use Git LFS: git lfs track '*.ckpt'"
    echo "   2. Download during build (add to Dockerfile)"
    echo "   3. Use pretrained model as fallback"
else
    echo "⚠️  Model checkpoint NOT found at models/acc1=76.2260.ckpt"
    echo "   You'll need to either:"
    echo "   1. Copy checkpoint to models/ folder"
    echo "   2. Download during Docker build"
    echo "   3. Use pretrained model"
fi
echo ""

# 5. Verify requirements.txt
echo "📋 Verifying requirements.txt..."
if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt found"
    echo "   Dependencies:"
    cat requirements.txt | grep -v "^#" | grep -v "^$"
else
    echo "❌ requirements.txt NOT found"
    exit 1
fi
echo ""

# 6. Check .gitignore
echo "🚫 Checking .gitignore..."
if grep -q "models/\*.ckpt" .gitignore; then
    echo "✅ Model checkpoints are gitignored"
else
    echo "⚠️  Model checkpoints may not be gitignored"
fi
echo ""

# 7. Summary
echo "========================================="
echo "✅ Preparation Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Review changes: git diff"
echo "2. Test locally: docker build -t imagenet-hf ."
echo "3. Create HF Space: https://huggingface.co/new-space"
echo "4. Add HF remote: git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/imagenet-vision-ai"
echo "5. Push to HF: git push hf main"
echo ""
echo "⚠️  IMPORTANT: Handle model checkpoint before pushing!"
echo "   See HUGGINGFACE_DEPLOYMENT.md for options"
echo ""

# 8. Create restore script
cat > restore_local.sh << 'EOF'
#!/bin/bash
# Restore local development files
echo "Restoring local files..."
cp Dockerfile.local Dockerfile
cp README.local.md README.md
cp .streamlit/config.local.toml .streamlit/config.toml
sed -i 's|checkpoint_path = "models/acc1=76.2260.ckpt"|checkpoint_path = "/home/ubuntu/imagenet/checkpoints/acc1=76.2260.ckpt"|g' app.py
echo "✅ Local files restored"
EOF
chmod +x restore_local.sh
echo "📝 Created restore_local.sh to revert changes"
echo ""
