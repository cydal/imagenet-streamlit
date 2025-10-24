# Dockerfile for Hugging Face Spaces deployment
# Read the doc: https://huggingface.co/docs/hub/spaces-sdks-docker

FROM python:3.9-slim

# Create user with UID 1000 (required for HF Spaces)
# Learn more about the Dev Mode at https://huggingface.co/dev-mode-explorers
RUN useradd -m -u 1000 user

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install (with proper ownership)
COPY --chown=user:user requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy application code (with proper ownership)
COPY --chown=user:user . /app

# Create directories with proper permissions
RUN mkdir -p /app/models /app/images && \
    chown -R user:user /app

# Switch to user
USER user

# Download model checkpoint from Hugging Face Hub
RUN pip install --no-cache-dir huggingface-hub && \
    python -c "from huggingface_hub import hf_hub_download; \
    hf_hub_download(repo_id='Sijuade/resnett50-imagenet', \
                    filename='acc1=76.2100.ckpt', \
                    local_dir='/app/models', \
                    local_dir_use_symlinks=False)"

# Set home to the user's home directory
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_PORT=7860 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Expose port 7860 (HF Spaces default)
EXPOSE 7860

# Run Streamlit on port 7860
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
