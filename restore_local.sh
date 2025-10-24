#\!/bin/bash
echo "Restoring local development files..."
cp Dockerfile.local Dockerfile 2>/dev/null || true
cp README.local.md README.md 2>/dev/null || true
cp .streamlit/config.local.toml .streamlit/config.toml 2>/dev/null || true
echo "✅ Local files restored"
