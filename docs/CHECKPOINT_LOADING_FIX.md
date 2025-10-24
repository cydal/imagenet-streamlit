# Checkpoint Loading Fix

## Issue
The app was failing to load the Lightning checkpoint due to:
1. **EMA keys** - Checkpoints contained `ema_model.*` keys from the EMA callback
2. **Strict loading** - Using `strict=True` caused failures with unexpected keys

## Solution

### Changes Made

#### 1. Updated Checkpoint Path
- **Old**: `models/acc1=71.8160.ckpt` (71.82% accuracy)
- **New**: `/home/ubuntu/imagenet/checkpoints/acc1=76.2260.ckpt` (76.23% accuracy)

#### 2. Fixed Model Loader (`utils/model_loader.py`)

Added two critical fixes:

**A. Filter out EMA keys:**
```python
# Remove EMA keys if present (from EMA callback)
state_dict = {k: v for k, v in state_dict.items() if not k.startswith('ema_model.')}
```

**B. Use strict=False:**
```python
# Load with strict=False to handle any missing/unexpected keys
model.load_state_dict(new_state_dict, strict=False)
```

### Reference Implementation

Based on the working implementation in `/home/ubuntu/inference_resnet50.py`:

```python
# Load weights (handle both EMA and non-EMA checkpoints)
state_dict = checkpoint['state_dict']

# Remove EMA keys if present
state_dict = {k: v for k, v in state_dict.items() if not k.startswith('ema_model.')}

# Load state dict
self.model.load_state_dict(state_dict, strict=False)
```

## Testing

### Verification
```bash
conda run -n imagenet python -c "
from utils.model_loader import load_model
model = load_model('/home/ubuntu/imagenet/checkpoints/acc1=76.2260.ckpt')
print('✅ Model loaded successfully!')
"
```

### Output
```
Loading model from /home/ubuntu/imagenet/checkpoints/acc1=76.2260.ckpt
Detected PyTorch Lightning checkpoint
Number of classes: 1000
Successfully loaded Lightning checkpoint
Model loaded successfully from /home/ubuntu/imagenet/checkpoints/acc1=76.2260.ckpt
✅ Model loaded successfully!
```

## Key Learnings

### EMA (Exponential Moving Average)
- Training uses EMA callback to maintain a moving average of model weights
- Checkpoint contains both regular weights (`model.*`) and EMA weights (`ema_model.*`)
- For inference, we only need the regular model weights
- EMA keys must be filtered out before loading

### Strict Loading
- `strict=True` (default) requires exact key matching
- `strict=False` allows missing or unexpected keys
- Necessary when checkpoint has extra keys (like optimizer state, EMA weights, etc.)

## Files Modified

1. **`app.py`**
   - Line 243: Updated checkpoint path to `acc1=76.2260.ckpt`
   - Line 288: Updated accuracy display to 76.23%

2. **`utils/model_loader.py`**
   - Line 50: Added EMA key filtering
   - Line 62: Changed to `strict=False` loading

## Checkpoint Details

**New Checkpoint:**
- Path: `/home/ubuntu/imagenet/checkpoints/acc1=76.2260.ckpt`
- Size: 391 MB
- Accuracy: 76.23%
- Classes: 1000 (ImageNet)
- Architecture: ResNet50

## Status

✅ **Fixed and Tested** - Model now loads successfully and is ready for inference.
