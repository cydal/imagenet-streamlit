# Upload Model to Hugging Face Hub

## Step 1: Install Hugging Face CLI

```bash
pip install huggingface_hub
```

## Step 2: Login to Hugging Face

```bash
huggingface-cli login
```

You'll be prompted to enter your HF token. Get it from: https://huggingface.co/settings/tokens

## Step 3: Create Model Repository

Go to https://huggingface.co/new and create a new model repository:
- **Name**: `imagenet-resnet50`
- **Type**: Model
- **Visibility**: Public (or Private)
- **License**: MIT (or your choice)

This will create: `https://huggingface.co/cydal/imagenet-resnet50`

## Step 4: Upload the Checkpoint

### Option A: Using CLI (Recommended)

```bash
# Upload the checkpoint file
huggingface-cli upload cydal/imagenet-resnet50 \
    models/acc1=76.2100.ckpt \
    acc1=76.2100.ckpt
```

### Option B: Using Python

```python
from huggingface_hub import HfApi

api = HfApi()

# Upload checkpoint
api.upload_file(
    path_or_fileobj="models/acc1=76.2100.ckpt",
    path_in_repo="acc1=76.2100.ckpt",
    repo_id="cydal/imagenet-resnet50",
    repo_type="model",
)

print("✅ Model uploaded successfully!")
```

### Option C: Using Git (For Large Files)

```bash
# Clone the repository
git clone https://huggingface.co/cydal/imagenet-resnet50
cd imagenet-resnet50

# Install Git LFS if not already installed
git lfs install

# Track large files
git lfs track "*.ckpt"
git add .gitattributes

# Copy and commit the checkpoint
cp ../streamlit-imagenet-app/models/acc1=76.2100.ckpt .
git add acc1=76.2100.ckpt
git commit -m "Add ResNet50 checkpoint (76.21% accuracy)"
git push
```

## Step 5: Create Model Card

Create a `README.md` in your model repository:

```markdown
---
license: mit
tags:
- image-classification
- pytorch
- resnet50
- imagenet
datasets:
- imagenet-1k
metrics:
- accuracy
model-index:
- name: ResNet50-ImageNet
  results:
  - task:
      type: image-classification
    dataset:
      name: ImageNet-1K
      type: imagenet-1k
    metrics:
    - type: accuracy
      value: 76.21
      name: Top-1 Accuracy
---

# ResNet50 - ImageNet Classifier

## Model Description

ResNet50 model trained on ImageNet-1K dataset achieving 76.21% top-1 accuracy.

### Model Details

- **Architecture**: ResNet50
- **Parameters**: 25.6M
- **Dataset**: ImageNet-1K (1000 classes)
- **Framework**: PyTorch + PyTorch Lightning
- **Training**: 
  - Optimizer: LAMB
  - Learning Rate: 0.005
  - Batch Size: 256 (8 GPUs)
  - Epochs: 300
  - Augmentation: RandAugment, Mixup, CutMix
  - Precision: Mixed (FP16)

### Performance

- **Top-1 Accuracy**: 76.21%
- **Input Size**: 224×224
- **Inference Time**: ~50-100ms (GPU)

## Usage

### Using the Streamlit App

Try the model at: [ImageNet Vision AI Space](https://huggingface.co/spaces/cydal/imagenet-vision-ai)

### Loading the Model

```python
import torch
from torchvision import models
from huggingface_hub import hf_hub_download

# Download checkpoint
checkpoint_path = hf_hub_download(
    repo_id="cydal/imagenet-resnet50",
    filename="acc1=76.2100.ckpt"
)

# Load checkpoint
checkpoint = torch.load(checkpoint_path, map_location='cpu')

# Initialize model
model = models.resnet50(weights=None)

# Extract and load state dict
state_dict = checkpoint['state_dict']
# Remove prefixes (model._orig_mod.)
new_state_dict = {}
for key, value in state_dict.items():
    if key.startswith('model._orig_mod.'):
        new_key = key[16:]
    elif key.startswith('model.'):
        new_key = key[6:]
    else:
        new_key = key
    new_state_dict[new_key] = value

model.load_state_dict(new_state_dict, strict=False)
model.eval()
```

### Inference Example

```python
from PIL import Image
from torchvision import transforms
import torch.nn.functional as F

# Preprocessing
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    ),
])

# Load and preprocess image
image = Image.open("image.jpg").convert('RGB')
input_tensor = preprocess(image).unsqueeze(0)

# Inference
with torch.no_grad():
    output = model(input_tensor)
    probabilities = F.softmax(output[0], dim=0)
    
# Get top-5 predictions
top5_prob, top5_idx = torch.topk(probabilities, 5)
for idx, prob in zip(top5_idx, top5_prob):
    print(f"Class {idx}: {prob.item()*100:.2f}%")
```

## Training Details

Trained using the ImageNet-Full-training codebase with:
- 8x GPU (DDP strategy)
- Mixed precision (FP16)
- Cosine learning rate schedule
- LAMB optimizer
- Data augmentation: RandAugment, Mixup (0.2), CutMix (1.0)
- Label smoothing (0.1)
- Random erasing (0.25)

## Limitations

- Trained only on ImageNet-1K (1000 classes)
- May not generalize well to out-of-distribution images
- Performance may vary on different image qualities

## Citation

```bibtex
@misc{imagenet-resnet50-2024,
  author = {Your Name},
  title = {ResNet50 ImageNet Classifier},
  year = {2024},
  publisher = {Hugging Face},
  howpublished = {\url{https://huggingface.co/cydal/imagenet-resnet50}}
}
```

## License

MIT License
```

## Step 6: Verify Upload

```bash
# Check if file exists
huggingface-cli scan-cache

# Or visit your model page
open https://huggingface.co/cydal/imagenet-resnet50
```

## Step 7: Test Download

```python
from huggingface_hub import hf_hub_download

# Test downloading
checkpoint_path = hf_hub_download(
    repo_id="cydal/imagenet-resnet50",
    filename="acc1=76.2100.ckpt",
    local_dir="./test_download"
)

print(f"✅ Downloaded to: {checkpoint_path}")
```

## Troubleshooting

### Authentication Error
```bash
# Re-login
huggingface-cli logout
huggingface-cli login
```

### Large File Error
```bash
# Use Git LFS for files > 5GB
git lfs install
git lfs track "*.ckpt"
```

### Upload Timeout
```bash
# Increase timeout
export HF_HUB_TIMEOUT=600
huggingface-cli upload ...
```

## Next Steps

After uploading:
1. ✅ Verify model appears on HF Hub
2. ✅ Test download works
3. ✅ Update Dockerfile.hf (already done)
4. ✅ Deploy to HF Spaces

---

**Your model will be available at**: `https://huggingface.co/cydal/imagenet-resnet50`
