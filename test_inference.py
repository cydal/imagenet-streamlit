#!/usr/bin/env python3
"""
Test script to verify the inference pipeline works correctly.
Tests both pretrained model and checkpoint loading (if available).
"""
import os
import sys
from pathlib import Path
import torch
from PIL import Image
import numpy as np

from utils.model_loader import load_model, get_model_info
from utils.image_processor import preprocess_image, get_top_predictions


def create_dummy_image():
    """Create a dummy RGB image for testing."""
    # Create a random 224x224 RGB image
    img_array = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    return Image.fromarray(img_array)


def test_pretrained_model():
    """Test loading and inference with pretrained model."""
    print("\n" + "="*60)
    print("TEST 1: Pretrained Model")
    print("="*60)
    
    try:
        # Load pretrained model
        print("Loading pretrained ResNet50...")
        model = load_model(model_path=None)
        
        # Get model info
        info = get_model_info(model)
        print(f"\nModel loaded successfully!")
        print(f"  Type: {info['model_type']}")
        print(f"  Parameters: {info['total_parameters']:,}")
        print(f"  Device: {info['device']}")
        
        # Create dummy image
        print("\nCreating test image...")
        image = create_dummy_image()
        
        # Preprocess
        print("Preprocessing image...")
        input_tensor = preprocess_image(image)
        print(f"  Input shape: {input_tensor.shape}")
        
        # Run inference
        print("Running inference...")
        with torch.no_grad():
            output = model(input_tensor)
            probabilities = torch.nn.functional.softmax(output[0], dim=0)
        
        print(f"  Output shape: {output.shape}")
        
        # Get predictions
        predictions = get_top_predictions(probabilities, top_k=5)
        
        print("\nTop 5 Predictions:")
        for idx, (class_name, confidence) in enumerate(predictions, 1):
            print(f"  {idx}. {class_name:40s} {confidence:6.2%}")
        
        print("\n✅ Pretrained model test PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Pretrained model test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_checkpoint_loading(checkpoint_path):
    """Test loading a Lightning checkpoint."""
    print("\n" + "="*60)
    print("TEST 2: Lightning Checkpoint Loading")
    print("="*60)
    
    if not os.path.exists(checkpoint_path):
        print(f"⚠️  Checkpoint not found: {checkpoint_path}")
        print("Skipping checkpoint test...")
        return None
    
    try:
        # Load checkpoint
        print(f"Loading checkpoint: {checkpoint_path}")
        model = load_model(model_path=checkpoint_path)
        
        # Get model info
        info = get_model_info(model)
        print(f"\nCheckpoint loaded successfully!")
        print(f"  Type: {info['model_type']}")
        print(f"  Parameters: {info['total_parameters']:,}")
        print(f"  Device: {info['device']}")
        
        # Create dummy image
        print("\nCreating test image...")
        image = create_dummy_image()
        
        # Preprocess
        print("Preprocessing image...")
        input_tensor = preprocess_image(image)
        
        # Run inference
        print("Running inference...")
        with torch.no_grad():
            output = model(input_tensor)
            probabilities = torch.nn.functional.softmax(output[0], dim=0)
        
        # Get predictions
        predictions = get_top_predictions(probabilities, top_k=5)
        
        print("\nTop 5 Predictions:")
        for idx, (class_name, confidence) in enumerate(predictions, 1):
            print(f"  {idx}. {class_name:40s} {confidence:6.2%}")
        
        print("\n✅ Checkpoint loading test PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Checkpoint loading test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("\n" + "="*60)
    print("ImageNet Inference Pipeline Test Suite")
    print("="*60)
    
    # Test 1: Pretrained model
    test1_passed = test_pretrained_model()
    
    # Test 2: Checkpoint loading (if available)
    checkpoint_paths = [
        "/home/ubuntu/imagenet/checkpoints/last.ckpt",
        "models/resnet50-epoch=89.ckpt",
    ]
    
    test2_result = None
    for ckpt_path in checkpoint_paths:
        if os.path.exists(ckpt_path):
            test2_result = test_checkpoint_loading(ckpt_path)
            break
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    print(f"Pretrained Model: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    
    if test2_result is None:
        print(f"Checkpoint Loading: ⚠️  SKIPPED (no checkpoint found)")
    else:
        print(f"Checkpoint Loading: {'✅ PASSED' if test2_result else '❌ FAILED'}")
    
    print("="*60 + "\n")
    
    # Exit code
    if test1_passed:
        print("✅ Core functionality verified!")
        sys.exit(0)
    else:
        print("❌ Tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
