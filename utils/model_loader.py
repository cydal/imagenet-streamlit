import torch
import torch.nn as nn
from torchvision import models
import os
import sys


def load_model(model_path=None):
    """
    Load a trained ImageNet model.
    Supports both PyTorch Lightning checkpoints and standard PyTorch checkpoints.
    
    Args:
        model_path (str, optional): Path to a saved model checkpoint.
                                   If None, loads a pretrained ResNet50.
    
    Returns:
        torch.nn.Module: Loaded model in evaluation mode
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    if model_path and os.path.exists(model_path):
        print(f"Loading model from {model_path}")
        
        # Try to load the checkpoint
        checkpoint = torch.load(model_path, map_location=device)
        
        # Check if this is a Lightning checkpoint
        if isinstance(checkpoint, dict) and 'state_dict' in checkpoint:
            # This is a Lightning checkpoint
            print("Detected PyTorch Lightning checkpoint")
            
            # Extract hyperparameters if available
            num_classes = 1000
            if 'hyper_parameters' in checkpoint:
                num_classes = checkpoint['hyper_parameters'].get('num_classes', 1000)
                print(f"Number of classes: {num_classes}")
            
            # Initialize ResNet50 model
            model = models.resnet50(weights=None)
            
            # Modify final layer if needed
            if num_classes != 1000:
                model.fc = nn.Linear(model.fc.in_features, num_classes)
            
            # Load state dict - Lightning wraps model in 'model' attribute
            state_dict = checkpoint['state_dict']
            
            # Remove 'model.' prefix from keys if present (Lightning wrapper)
            new_state_dict = {}
            for key, value in state_dict.items():
                if key.startswith('model.'):
                    new_key = key[6:]  # Remove 'model.' prefix
                    new_state_dict[new_key] = value
                else:
                    new_state_dict[key] = value
            
            model.load_state_dict(new_state_dict)
            print(f"Successfully loaded Lightning checkpoint")
            
        elif isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
            # Standard PyTorch checkpoint format
            print("Detected standard PyTorch checkpoint")
            model = models.resnet50(weights=None)
            model.load_state_dict(checkpoint['model_state_dict'])
            
        else:
            # Direct state dict
            print("Detected direct state dict")
            model = models.resnet50(weights=None)
            model.load_state_dict(checkpoint)
        
        print(f"Model loaded successfully from {model_path}")
    else:
        # Load pretrained model as default
        if model_path:
            print(f"Warning: Model path '{model_path}' does not exist")
        print("Loading pretrained ResNet50 model from torchvision")
        model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)
    
    model.to(device)
    model.eval()
    
    return model


def get_model_info(model):
    """
    Get information about the model.
    
    Args:
        model: PyTorch model
    
    Returns:
        dict: Model information
    """
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    
    return {
        "total_parameters": total_params,
        "trainable_parameters": trainable_params,
        "device": next(model.parameters()).device,
        "model_type": type(model).__name__
    }
