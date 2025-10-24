import streamlit as st
import torch
import torch.nn as nn
from PIL import Image
import numpy as np
from torchvision import transforms
import json
import os
import time
from typing import List, Tuple
from pathlib import Path
from utils.model_loader import load_model, get_model_info
from utils.image_processor import preprocess_image, get_top_predictions


# Page configuration
st.set_page_config(
    page_title="ImageNet Vision AI - Deep Learning Inference",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/imagenet-inference',
        'Report a bug': "https://github.com/yourusername/imagenet-inference/issues",
        'About': "# ImageNet Vision AI\nPowered by PyTorch and Streamlit"
    }
)

# Custom CSS for beautiful UI
st.markdown("""
    <style>
    /* Main header styling */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        letter-spacing: -1px;
    }
    
    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    /* Upload section styling */
    .upload-section {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 20px;
        border: 2px dashed #667eea;
        text-align: center;
        margin: 1rem 0;
    }
    
    /* Prediction card styling */
    .prediction-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        transition: transform 0.2s;
    }
    
    .prediction-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .rank-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: bold;
        font-size: 1.1rem;
        margin-right: 1rem;
    }
    
    .class-name {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1f2937;
        margin: 0.5rem 0;
    }
    
    .confidence-text {
        font-size: 1.1rem;
        color: #6b7280;
        font-weight: 500;
    }
    
    /* Image container */
    .image-container {
        background: white;
        padding: 1rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    /* Stats styling */
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: bold;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* Progress bar custom styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Button styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_model(model_path=None):
    """Load and cache the model"""
    return load_model(model_path)


def get_sample_images():
    """Get list of sample images from the images folder."""
    images_dir = Path("images")
    if not images_dir.exists():
        return []
    
    # Get all image files
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.webp', '*.gif']
    sample_images = []
    
    for ext in image_extensions:
        sample_images.extend(images_dir.glob(ext))
        sample_images.extend(images_dir.glob(ext.upper()))
    
    return sorted(sample_images)


def process_single_image(image: Image.Image, model, top_k: int, threshold: float) -> Tuple[List, float]:
    """Process a single image and return predictions with inference time."""
    start_time = time.time()
    
    # Preprocess image
    input_tensor = preprocess_image(image)
    
    # Make prediction
    with torch.no_grad():
        output = model(input_tensor)
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
    
    # Get top predictions
    predictions = get_top_predictions(
        probabilities,
        top_k=top_k,
        threshold=threshold
    )
    
    inference_time = time.time() - start_time
    return predictions, inference_time


def display_prediction_card(rank: int, class_name: str, confidence: float, is_top: bool = False):
    """Display a beautiful prediction card."""
    # Color scheme based on rank
    if rank == 1:
        gradient = "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
        emoji = "🥇"
    elif rank == 2:
        gradient = "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"
        emoji = "🥈"
    elif rank == 3:
        gradient = "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)"
        emoji = "🥉"
    else:
        gradient = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
        emoji = "🎯"
    
    # Confidence color
    if confidence >= 0.7:
        conf_color = "#10b981"  # Green
    elif confidence >= 0.4:
        conf_color = "#f59e0b"  # Orange
    else:
        conf_color = "#6b7280"  # Gray
    
    st.markdown(f"""
        <div class="prediction-card" style="border-left-color: {conf_color};">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div style="flex: 1;">
                    <span style="font-size: 2rem; margin-right: 1rem;">{emoji}</span>
                    <span class="rank-badge" style="background: {gradient};">#{rank}</span>
                    <div class="class-name">{class_name}</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 2.5rem; font-weight: bold; color: {conf_color};">
                        {confidence:.1%}
                    </div>
                    <div class="confidence-text">Confidence</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Progress bar
    st.progress(confidence)


def main():
    # Header with gradient
    st.markdown('<h1 class="main-header">🖼️ ImageNet Vision AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Powered by Deep Learning • Upload images and get instant predictions</p>', unsafe_allow_html=True)
    
    # Hardcoded checkpoint path
    checkpoint_path = "/home/ubuntu/imagenet/checkpoints/acc1=76.2260.ckpt"
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # Inference settings
        st.markdown("### 🎯 Inference Settings")
        
        top_k = st.slider(
            "Top predictions",
            min_value=1,
            max_value=10,
            value=5,
            help="Number of top predictions to display"
        )
        
        confidence_threshold = st.slider(
            "Confidence threshold",
            min_value=0,
            max_value=100,
            value=0,
            help="Filter predictions below this confidence"
        ) / 100.0
        
        st.markdown("---")
        
        # Advanced options
        with st.expander("🔧 Advanced Options"):
            show_model_info = st.checkbox("Show model information", value=False)
            show_inference_time = st.checkbox("Show inference time", value=True)
        
        st.markdown("---")
        
        # Info section
        st.markdown("### ℹ️ About")
        st.markdown("""
        **Features:**
        - 🎨 Drag & drop multiple images
        - ⚡ Real-time inference
        - 📊 Beautiful visualizations
        - 💾 Export predictions to JSON
        
        **Model:**
        - ResNet50 trained on ImageNet
        - Accuracy: 76.23%
        - 1000 classes
        """)
    
    # Load model once
    with st.spinner("🔄 Loading model..."):
        try:
            model = initialize_model(checkpoint_path)
            
            if show_model_info:
                info = get_model_info(model)
                st.success(f"✅ Model loaded: {info['model_type']} ({info['total_parameters']:,} parameters)")
        except Exception as e:
            st.error(f"❌ Error loading model: {str(e)}")
            return
    
    # Main upload section with drag and drop
    st.markdown("---")
    st.markdown("### 📤 Upload Images")
    st.markdown("Drag and drop images below, or click to browse")
    
    uploaded_files = st.file_uploader(
        "Choose images",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    
    if uploaded_files:
        # Stats row
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
                <div class="stat-box">
                    <div class="stat-value">{len(uploaded_files)}</div>
                    <div class="stat-label">Images Uploaded</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            device_name = "GPU" if torch.cuda.is_available() else "CPU"
            st.markdown(f"""
                <div class="stat-box">
                    <div class="stat-value">{device_name}</div>
                    <div class="stat-label">Processing Device</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="stat-box">
                    <div class="stat-value">{top_k}</div>
                    <div class="stat-label">Top Predictions</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Process each image
        all_results = []
        
        for idx, uploaded_file in enumerate(uploaded_files):
            st.markdown(f"## 🖼️ Image {idx + 1}: {uploaded_file.name}")
            
            # Create two columns for image and predictions
            img_col, pred_col = st.columns([1, 1])
            
            with img_col:
                # Load and display image
                try:
                    image = Image.open(uploaded_file).convert('RGB')
                    
                    # Display image in a nice container
                    st.markdown('<div class="image-container">', unsafe_allow_html=True)
                    st.image(image, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Image metadata
                    st.caption(f"📐 Dimensions: {image.size[0]} × {image.size[1]} pixels")
                    st.caption(f"📁 Format: {image.format if hasattr(image, 'format') else 'Unknown'}")
                    
                except Exception as e:
                    st.error(f"❌ Error loading image: {str(e)}")
                    continue
            
            with pred_col:
                # Run inference
                with st.spinner("🔮 Analyzing image..."):
                    try:
                        predictions, inference_time = process_single_image(
                            image, model, top_k, confidence_threshold
                        )
                        
                        if show_inference_time:
                            st.info(f"⚡ Inference time: {inference_time*1000:.1f}ms")
                        
                        if predictions:
                            st.markdown("### 🎯 Predictions")
                            
                            # Display prediction cards
                            for rank, (class_name, confidence) in enumerate(predictions, 1):
                                display_prediction_card(rank, class_name, confidence)
                            
                            # Store results for batch export
                            all_results.append({
                                "image": uploaded_file.name,
                                "predictions": [
                                    {"rank": i+1, "class": c, "confidence": float(conf)}
                                    for i, (c, conf) in enumerate(predictions)
                                ],
                                "inference_time_ms": inference_time * 1000
                            })
                        else:
                            st.warning(f"⚠️ No predictions above {confidence_threshold:.0%} confidence threshold")
                    
                    except Exception as e:
                        st.error(f"❌ Error during inference: {str(e)}")
                        st.exception(e)
            
            # Separator between images
            if idx < len(uploaded_files) - 1:
                st.markdown("---")
        
        # Batch download option
        if all_results:
            st.markdown("---")
            st.markdown("### 💾 Export Results")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("Download all predictions as JSON")
            
            with col2:
                results_json = json.dumps({
                    "model": checkpoint_path,
                    "total_images": len(uploaded_files),
                    "results": all_results
                }, indent=2)
                
                st.download_button(
                    label="📥 Download All Results",
                    data=results_json,
                    file_name=f"predictions_{len(uploaded_files)}_images.json",
                    mime="application/json",
                    use_container_width=True
                )
    
    else:
        # Empty state with beautiful design
        st.markdown("""
            <div class="upload-section">
                <h2 style="color: #667eea; margin-bottom: 1rem;">📸 No Images Yet</h2>
                <p style="font-size: 1.1rem; color: #6b7280; margin-bottom: 1.5rem;">
                    Drag and drop your images here, or click the button above to browse
                </p>
                <p style="color: #9ca3af;">
                    Supported formats: JPG, JPEG, PNG, WebP<br>
                    You can upload multiple images at once!
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Show sample images if available
        sample_images = get_sample_images()
        if sample_images:
            st.markdown("---")
            st.markdown("### 🎨 Try Sample Images")
            st.markdown("Click on a sample image below to run predictions")
            
            # Display sample images in a grid
            cols_per_row = 4
            for i in range(0, len(sample_images), cols_per_row):
                cols = st.columns(cols_per_row)
                for j, col in enumerate(cols):
                    idx = i + j
                    if idx < len(sample_images):
                        img_path = sample_images[idx]
                        with col:
                            try:
                                img = Image.open(img_path)
                                st.image(img, use_container_width=True)
                                
                                # Button to run prediction on this image
                                if st.button(f"Predict", key=f"sample_{idx}"):
                                    st.session_state['selected_sample'] = str(img_path)
                                    st.rerun()
                                    
                                st.caption(img_path.name)
                            except Exception as e:
                                st.error(f"Error loading {img_path.name}")
        
        # Process selected sample image
        if 'selected_sample' in st.session_state:
            sample_path = st.session_state['selected_sample']
            del st.session_state['selected_sample']
            
            st.markdown("---")
            st.markdown(f"## 🖼️ Sample Image: {Path(sample_path).name}")
            
            img_col, pred_col = st.columns([1, 1])
            
            with img_col:
                try:
                    image = Image.open(sample_path).convert('RGB')
                    st.markdown('<div class="image-container">', unsafe_allow_html=True)
                    st.image(image, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.caption(f"📐 Dimensions: {image.size[0]} × {image.size[1]} pixels")
                except Exception as e:
                    st.error(f"❌ Error loading image: {str(e)}")
            
            with pred_col:
                with st.spinner("🔮 Analyzing image..."):
                    try:
                        predictions, inference_time = process_single_image(
                            image, model, top_k, confidence_threshold
                        )
                        
                        if show_inference_time:
                            st.info(f"⚡ Inference time: {inference_time*1000:.1f}ms")
                        
                        if predictions:
                            st.markdown("### 🎯 Predictions")
                            
                            for rank, (class_name, confidence) in enumerate(predictions, 1):
                                display_prediction_card(rank, class_name, confidence)
                        else:
                            st.warning(f"⚠️ No predictions above {confidence_threshold:.0%} confidence threshold")
                    
                    except Exception as e:
                        st.error(f"❌ Error during inference: {str(e)}")
                        st.exception(e)
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <p style='color: #9ca3af; font-size: 0.9rem;'>
                Built with ❤️ using Streamlit & PyTorch<br>
                <strong>ImageNet Vision AI</strong> • Powered by Deep Learning
            </p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
