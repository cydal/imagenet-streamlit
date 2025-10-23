import torch
from torchvision import transforms
from PIL import Image
import json
import os


# ImageNet normalization parameters
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]


def get_transform():
    """
    Get the standard ImageNet preprocessing transform.
    
    Returns:
        torchvision.transforms.Compose: Transform pipeline
    """
    return transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD)
    ])


def preprocess_image(image):
    """
    Preprocess an image for model inference.
    
    Args:
        image (PIL.Image): Input image
    
    Returns:
        torch.Tensor: Preprocessed image tensor with batch dimension
    """
    transform = get_transform()
    image_tensor = transform(image)
    # Add batch dimension
    image_tensor = image_tensor.unsqueeze(0)
    
    # Move to GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    image_tensor = image_tensor.to(device)
    
    return image_tensor


def load_class_labels(labels_path=None):
    """
    Load ImageNet class labels.
    
    Args:
        labels_path (str, optional): Path to custom labels JSON file
    
    Returns:
        dict: Dictionary mapping class indices to class names
    """
    if labels_path and os.path.exists(labels_path):
        with open(labels_path, 'r') as f:
            return json.load(f)
    
    # Default ImageNet class names (simplified version)
    # In production, you should include all 1000 classes
    # This is a placeholder - you can load from a file or use imagenet_classes
    try:
        # Try to load from a standard location
        import urllib.request
        url = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
        with urllib.request.urlopen(url) as response:
            labels = json.loads(response.read().decode())
            return {i: label for i, label in enumerate(labels)}
    except:
        # Fallback to generic labels
        return {i: f"class_{i}" for i in range(1000)}


def get_top_predictions(probabilities, top_k=5, threshold=0.0):
    """
    Get top K predictions from model output.
    
    Args:
        probabilities (torch.Tensor): Softmax probabilities from model
        top_k (int): Number of top predictions to return
        threshold (float): Minimum confidence threshold (0-1)
    
    Returns:
        list: List of tuples (class_name, confidence)
    """
    # Load class labels
    class_labels = load_class_labels()
    
    # Get top K predictions
    top_probs, top_indices = torch.topk(probabilities, k=min(top_k, len(probabilities)))
    
    predictions = []
    for prob, idx in zip(top_probs, top_indices):
        prob_value = prob.item()
        if prob_value >= threshold:
            class_idx = idx.item()
            class_name = class_labels.get(class_idx, f"Unknown (class {class_idx})")
            predictions.append((class_name, prob_value))
    
    return predictions


def denormalize_image(tensor):
    """
    Denormalize an image tensor for visualization.
    
    Args:
        tensor (torch.Tensor): Normalized image tensor
    
    Returns:
        torch.Tensor: Denormalized image tensor
    """
    mean = torch.tensor(IMAGENET_MEAN).view(3, 1, 1)
    std = torch.tensor(IMAGENET_STD).view(3, 1, 1)
    
    return tensor * std + mean
