#!/usr/bin/env python3
"""
Standalone inference script for ImageNet model.
Can be used independently of the Streamlit app.

Usage:
    python inference.py --image path/to/image.jpg --checkpoint path/to/checkpoint.ckpt
    python inference.py --image path/to/image.jpg  # Uses pretrained model
"""
import argparse
import torch
from PIL import Image
import json

from utils.model_loader import load_model, get_model_info
from utils.image_processor import preprocess_image, get_top_predictions


def main():
    parser = argparse.ArgumentParser(description="ImageNet Model Inference")
    parser.add_argument("--image", type=str, required=True,
                        help="Path to input image")
    parser.add_argument("--checkpoint", type=str, default=None,
                        help="Path to model checkpoint (optional, uses pretrained if not provided)")
    parser.add_argument("--top_k", type=int, default=5,
                        help="Number of top predictions to show")
    parser.add_argument("--threshold", type=float, default=0.0,
                        help="Confidence threshold (0-1)")
    parser.add_argument("--output", type=str, default=None,
                        help="Output JSON file path (optional)")
    parser.add_argument("--verbose", action="store_true",
                        help="Print model information")
    
    args = parser.parse_args()
    
    # Load model
    print(f"\n{'='*60}")
    print("Loading model...")
    print(f"{'='*60}")
    model = load_model(args.checkpoint)
    
    if args.verbose:
        info = get_model_info(model)
        print(f"\nModel Information:")
        print(f"  Type: {info['model_type']}")
        print(f"  Total parameters: {info['total_parameters']:,}")
        print(f"  Trainable parameters: {info['trainable_parameters']:,}")
        print(f"  Device: {info['device']}")
    
    # Load and preprocess image
    print(f"\n{'='*60}")
    print(f"Processing image: {args.image}")
    print(f"{'='*60}")
    
    try:
        image = Image.open(args.image).convert('RGB')
        print(f"Image size: {image.size[0]} x {image.size[1]} pixels")
    except Exception as e:
        print(f"Error loading image: {e}")
        return
    
    input_tensor = preprocess_image(image)
    
    # Run inference
    print(f"\n{'='*60}")
    print("Running inference...")
    print(f"{'='*60}")
    
    with torch.no_grad():
        output = model(input_tensor)
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
    
    # Get predictions
    predictions = get_top_predictions(
        probabilities,
        top_k=args.top_k,
        threshold=args.threshold
    )
    
    # Display results
    print(f"\n{'='*60}")
    print(f"Top {args.top_k} Predictions:")
    print(f"{'='*60}")
    
    if predictions:
        for idx, (class_name, confidence) in enumerate(predictions, 1):
            print(f"{idx}. {class_name:40s} {confidence:6.2%}")
    else:
        print(f"No predictions above {args.threshold:.0%} confidence threshold")
    
    print(f"{'='*60}\n")
    
    # Save to JSON if requested
    if args.output:
        output_data = {
            "image": args.image,
            "checkpoint": args.checkpoint if args.checkpoint else "pretrained",
            "predictions": [
                {
                    "rank": i + 1,
                    "class": class_name,
                    "confidence": float(confidence)
                }
                for i, (class_name, confidence) in enumerate(predictions)
            ]
        }
        
        with open(args.output, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"Results saved to: {args.output}\n")


if __name__ == "__main__":
    main()
