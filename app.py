import streamlit as st
import torch
import torch.nn as nn
from PIL import Image
import numpy as np
from torchvision import transforms
import json
import os
from utils.model_loader import load_model
from utils.image_processor import preprocess_image, get_top_predictions


# Page configuration
st.set_page_config(
    page_title="ImageNet Model Inference",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .prediction-box {
        padding: 1rem;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_model(model_path=None):
    """Load and cache the model"""
    return load_model(model_path)


def main():
    # Header
    st.markdown('<h1 class="main-header">🖼️ ImageNet Model Inference</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Model selection
        model_path = st.text_input(
            "Model Path (optional)",
            placeholder="/path/to/model.pth",
            help="Leave empty to use default pretrained model"
        )
        
        # Top-K predictions
        top_k = st.slider(
            "Number of predictions to show",
            min_value=1,
            max_value=10,
            value=5,
            help="Show top K predictions"
        )
        
        # Confidence threshold
        confidence_threshold = st.slider(
            "Confidence Threshold (%)",
            min_value=0,
            max_value=100,
            value=0,
            help="Filter predictions below this confidence"
        ) / 100.0
        
        st.markdown("---")
        st.markdown("### About")
        st.info(
            "This application performs inference on images using a trained ImageNet model. "
            "Upload an image to get predictions with confidence scores."
        )
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📤 Upload Image")
        uploaded_file = st.file_uploader(
            "Choose an image...",
            type=["jpg", "jpeg", "png"],
            help="Upload an image for classification"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file).convert('RGB')
            st.image(image, caption="Uploaded Image", use_container_width=True)
            
            # Image info
            st.caption(f"Image size: {image.size[0]} x {image.size[1]} pixels")
    
    with col2:
        st.subheader("🎯 Predictions")
        
        if uploaded_file is not None:
            with st.spinner("Loading model..."):
                try:
                    model = initialize_model(model_path if model_path else None)
                except Exception as e:
                    st.error(f"Error loading model: {str(e)}")
                    return
            
            with st.spinner("Processing image..."):
                try:
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
                        threshold=confidence_threshold
                    )
                    
                    if predictions:
                        # Display predictions
                        for idx, (class_name, confidence) in enumerate(predictions, 1):
                            with st.container():
                                st.markdown(f"""
                                    <div class="prediction-box">
                                        <strong>#{idx}: {class_name}</strong><br>
                                        Confidence: {confidence:.2%}
                                    </div>
                                """, unsafe_allow_html=True)
                                
                                # Progress bar for confidence
                                st.progress(confidence)
                        
                        # Download predictions
                        st.markdown("---")
                        predictions_json = json.dumps(
                            [{"rank": i+1, "class": c, "confidence": f"{conf:.4f}"} 
                             for i, (c, conf) in enumerate(predictions)],
                            indent=2
                        )
                        st.download_button(
                            label="📥 Download Predictions (JSON)",
                            data=predictions_json,
                            file_name="predictions.json",
                            mime="application/json"
                        )
                    else:
                        st.warning(f"No predictions above {confidence_threshold:.0%} confidence threshold.")
                    
                except Exception as e:
                    st.error(f"Error during inference: {str(e)}")
                    st.exception(e)
        else:
            st.info("👆 Upload an image to see predictions")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "Built with Streamlit 🎈 | Powered by PyTorch 🔥"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
