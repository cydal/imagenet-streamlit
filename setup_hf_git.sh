#\!/bin/bash
# Setup HF git authentication

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   Setup HF Spaces Git Authentication                       ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "You need to add your HF token to the git remote URL"
echo ""
echo "Step 1: Get your HF token"
echo "  → Visit: https://huggingface.co/settings/tokens"
echo "  → Copy your token (starts with hf_...)"
echo ""
echo "Step 2: Enter your credentials below"
echo ""

read -p "HF Username (e.g., Sijuade): " HF_USER
read -sp "HF Token (paste here, won't be visible): " HF_TOKEN
echo ""
echo ""

# Update remote with credentials
git remote remove hf 2>/dev/null || true
git remote add hf https://${HF_USER}:${HF_TOKEN}@huggingface.co/spaces/Sijuade/imagenet-resnet50-inference

echo "✅ Git remote configured with authentication"
echo ""
echo "Now pushing to HF Spaces..."
echo ""

# Push with force (since histories don't match)
git push hf main --force

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║   Deployment Complete\!                                      ║"
echo "║   Visit: https://huggingface.co/spaces/Sijuade/imagenet-resnet50-inference"
echo "╚════════════════════════════════════════════════════════════╝"
