# Fix: Git Push Authentication to HF Spaces

## Problem
Git push to HF Spaces is stuck because it's waiting for authentication credentials.

## Solution: Use HF Token in Remote URL

### Step 1: Get Your HF Token

1. Go to: https://huggingface.co/settings/tokens
2. Create a new token (or use existing)
3. Copy the token (starts with `hf_...`)

### Step 2: Update Git Remote with Token

```bash
# Remove current remote
git remote remove hf

# Add remote with token (replace YOUR_TOKEN)
git remote add hf https://YOUR_USERNAME:YOUR_TOKEN@huggingface.co/spaces/Sijuade/imagenet-resnet50-inference
```

**Example:**
```bash
git remote add hf https://Sijuade:hf_xxxxxxxxxxxxxxxxxxxx@huggingface.co/spaces/Sijuade/imagenet-resnet50-inference
```

### Step 3: Push Again

```bash
git push hf main
```

## Alternative: Use HF CLI

### Option 1: Login with HF CLI

```bash
# Install HF CLI if not installed
pip install huggingface_hub

# Login (will prompt for token)
huggingface-cli login

# Then push normally
git push hf main
```

### Option 2: Use Git Credential Helper

```bash
# Configure git to use HF token
git config --global credential.helper store

# Push (will prompt for credentials once)
git push hf main
# Username: Sijuade
# Password: hf_your_token_here
```

## Quick Fix Script

```bash
#!/bin/bash
# Quick fix for HF authentication

echo "Enter your HF username (e.g., Sijuade):"
read HF_USERNAME

echo "Enter your HF token (from https://huggingface.co/settings/tokens):"
read -s HF_TOKEN

# Update remote
git remote remove hf 2>/dev/null || true
git remote add hf https://${HF_USERNAME}:${HF_TOKEN}@huggingface.co/spaces/Sijuade/imagenet-resnet50-inference

echo "✅ Remote updated with authentication"
echo "Now run: git push hf main"
```

## Verify Remote

```bash
# Check remote (token will be hidden)
git remote -v

# Should show:
# hf  https://Sijuade:***@huggingface.co/spaces/Sijuade/imagenet-resnet50-inference (fetch)
# hf  https://Sijuade:***@huggingface.co/spaces/Sijuade/imagenet-resnet50-inference (push)
```

## Security Note

⚠️ **Never commit your token to git!**

The token in the remote URL is stored in `.git/config` which is not committed.

## Test Push

```bash
# Small test push
git push hf main

# Should see:
# Enumerating objects...
# Counting objects...
# Writing objects...
# remote: Updating branch 'main'
# To https://huggingface.co/spaces/Sijuade/imagenet-resnet50-inference
#    abc123..def456  main -> main
```

---

**After fixing authentication, your push should complete in 1-2 minutes!**
