import torch
import torch.nn as nn
from torchvision import models
import os


def load_model(model_path=None):
    """
    Load a trained ImageNet model.
    
    Args:
        model_path (str, optional): Path to a saved model checkpoint.
                                   If None, loads a pretrained ResNet50.
    
    Returns:
        torch.nn.Module: Loaded model in evaluation mode
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    if model_path and os.path.exists(model_path):
        # Load custom trained model
        print(f"Loading model from {model_path}")
        
        # Try to load the checkpoint
        checkpoint = torch.load(model_path, map_location=device)
        
        # Initialize model architecture (modify based on your model)
        # This is a placeholder - adjust according to your model architecture
        model = models.resnet50(pretrained=False)
        
        # Load state dict
        if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
            model.load_state_dict(checkpoint['model_state_dict'])
        elif isinstance(checkpoint, dict) and 'state_dict' in checkpoint:
            model.load_state_dict(checkpoint['state_dict'])
        else:
            model.load_state_dict(checkpoint)
        
        print(f"Model loaded successfully from {model_path}")
    else:
        # Load pretrained model as default
        print("Loading pretrained ResNet50 model")
        model = models.resnet50(pretrained=True)
    
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
