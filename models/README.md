# Models Directory

Place your trained model checkpoints here.

## Usage

### Copy from Training Directory

```bash
# Copy a trained checkpoint
cp /home/ubuntu/imagenet/checkpoints/resnet50-epoch=89-val_acc1=0.7500.ckpt .

# Or copy the latest checkpoint
cp /home/ubuntu/imagenet/checkpoints/last.ckpt .
```

### Use in Docker

When running the Streamlit app in Docker, reference the checkpoint as:
```
/app/models/resnet50-epoch=89-val_acc1=0.7500.ckpt
```

The `models/` directory is mounted as a volume in Docker, so you can:
1. Add/update checkpoints without rebuilding the container
2. Access them from the Streamlit UI

### Supported Formats

- **PyTorch Lightning checkpoints** (.ckpt)
- **Standard PyTorch checkpoints** (.pth, .pt)

## Example

```bash
# List available checkpoints
ls -lh

# Test inference with a checkpoint
cd ..
python inference.py \
    --image test_image.jpg \
    --checkpoint models/resnet50-epoch=89.ckpt \
    --verbose
```
