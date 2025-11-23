"""
Enhanced Streamlit app with CLAHE preprocessing and disease information
"""

import streamlit as st
import tensorflow as tf
from tensorflow import keras
from PIL import Image
import numpy as np
import os

# Try to import CV2 for CLAHE, fall back to basic preprocessing if not available
try:
    import cv2
    CLAHE_AVAILABLE = True
except ImportError:
    CLAHE_AVAILABLE = False
    st.warning("OpenCV not available. Install it for better preprocessing: pip install opencv-python")

# Import utilities if available
try:
    from utils import preprocess_with_clahe, get_disease_info
    UTILS_AVAILABLE = True
except ImportError:
    UTILS_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="Plant Disease Detection",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #558B2F;
        text-align: center;
        margin-bottom: 2rem;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .healthy-box {
        background-color: #E8F5E9;
        border-left: 5px solid #4CAF50;
    }
    .disease-box {
        background-color: #FFF3E0;
        border-left: 5px solid #FF9800;
    }
</style>
""", unsafe_allow_html=True)

# Class labels
CLASS_LABELS = [
    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
    'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
    'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight',
    'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy',
    'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy',
    'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight',
    'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

@st.cache_resource
def load_model():
    """Load the trained model"""
    model_path = 'models/best_model.h5'
    os.makedirs('models', exist_ok=True)
    
    # If model doesn't exist locally, try to download it
    if not os.path.exists(model_path):
        st.info("📥 Downloading model from cloud storage...")
        try:
            import gdown
            # TODO: Replace with your model's public URL
            # Example for Google Drive:
            # file_id = 'YOUR_GOOGLE_DRIVE_FILE_ID'
            # url = f'https://drive.google.com/uc?id={file_id}'
            # gdown.download(url, model_path, quiet=False)
            
            # For now, show setup instructions
            st.warning("⚠️ Model file not found. Please configure model download.")
            st.info("""
            **To enable automatic model download:**
            
            1. Upload your `best_model.h5` to Google Drive
            2. Make it publicly accessible (Anyone with link can view)
            3. Get the file ID from the share link
            4. Set it as a Streamlit secret or environment variable
            
            **Alternative:** Use Hugging Face Hub or GitHub LFS
            """)
            return None
        except Exception as e:
            st.error(f"Error setting up model: {str(e)}")
            return None
    
    try:
        model = keras.models.load_model(model_path)
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

def preprocess_image(image, target_size=(224, 224), use_clahe=False):
    """Preprocess the uploaded image"""
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    image = image.resize(target_size)
    img_array = np.array(image)
    
    # Apply CLAHE if available and requested
    if use_clahe and CLAHE_AVAILABLE and UTILS_AVAILABLE:
        from utils import apply_clahe
        img_array = apply_clahe(img_array)
    
    img_array = img_array.astype('float32') / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

def predict_disease(model, image, use_clahe=False):
    """Make prediction on the image"""
    processed_image = preprocess_image(image, use_clahe=use_clahe)
    predictions = model.predict(processed_image, verbose=0)
    predicted_class = np.argmax(predictions[0])
    confidence = predictions[0][predicted_class]
    
    return CLASS_LABELS[predicted_class], confidence, predictions[0]

def main():
    # Header
    st.markdown('<h1 class="main-header">🌿 Plant Disease Detection System</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Agricultural Disease Diagnosis</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/leaf.png", width=80)
        st.header("⚙️ Settings")
        
        # Preprocessing option
        use_clahe = st.checkbox(
            "Use CLAHE Preprocessing",
            value=CLAHE_AVAILABLE,
            help="Contrast Limited Adaptive Histogram Equalization for better image quality",
            disabled=not CLAHE_AVAILABLE
        )
        
        st.markdown("---")
        st.header("📊 Model Information")
        st.info("""
        **Supported Architectures:**
        - VGG16/VGG19
        - ResNet50
        - DenseNet121
        - EfficientNetB5
        - ConvNextLarge
        - AlexNet
        
        **Dataset:** PlantVillage with CLAHE preprocessing
        
        **Classes:** 38 plant-disease combinations
        """)
        
        st.markdown("---")
        st.header("📖 Instructions")
        st.markdown("""
        1. 📤 Upload a clear leaf image
        2. ⚙️ Choose preprocessing options
        3. 🔍 View prediction results
        4. 💊 Get treatment recommendations
        """)
        
        st.markdown("---")
        st.header("🔗 Links")
        st.markdown("""
        - [🤗 Hugging Face Demo](https://huggingface.co/spaces/gyanbardhan123/PlantDiseaseDetection)
        - [📁 GitHub Repository](https://github.com/Gyanbardhan/PlantDiseaseDetection)
        - [📚 Documentation](Documentation.pdf)
        """)
    
    # Load model
    model = load_model()
    
    if model is None:
        st.error("❌ Model file not found!")
        st.markdown("""
        ### 🛠️ Setup Instructions:
        1. Create a `models` folder
        2. Download a pre-trained model:
           - [VGG16 Model](https://www.kaggle.com/datasets/gyanbardhan/vgg16)
           - [VGG19 Model](https://www.kaggle.com/datasets/clay108/vgg19-123)
           - [AlexNet Model](https://www.kaggle.com/datasets/gyanbardhan/alexnet123)
        3. Place it as `models/best_model.h5`
        4. Refresh this page
        """)
        return
    
    # File uploader
    st.markdown("### 📤 Upload Plant Leaf Image")
    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=['jpg', 'jpeg', 'png'],
        help="Upload a clear, well-lit image of a plant leaf"
    )
    
    # Example images section
    with st.expander("💡 View Example Images"):
        st.info("For best results, upload images similar to those used in training: clear, centered leaf images with good lighting.")
    
    if uploaded_file is not None:
        # Create columns
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📷 Uploaded Image")
            image = Image.open(uploaded_file)
            st.image(image, use_container_width=True)
            
            # Image info
            st.caption(f"Size: {image.size[0]}x{image.size[1]} pixels | Format: {image.format}")
        
        with col2:
            st.subheader("🔬 Analysis Results")
            
            with st.spinner("🔄 Analyzing image..."):
                try:
                    # Make prediction
                    predicted_label, confidence, all_predictions = predict_disease(
                        model, image, use_clahe=use_clahe
                    )
                    
                    # Parse prediction
                    parts = predicted_label.split('___')
                    plant_name = parts[0].replace('_', ' ')
                    disease_name = parts[1].replace('_', ' ') if len(parts) > 1 else 'Unknown'
                    
                    # Display main result
                    is_healthy = disease_name.lower() == 'healthy'
                    
                    if is_healthy:
                        st.markdown(f"""
                        <div class="info-box healthy-box">
                            <h3>✅ Healthy Plant Detected!</h3>
                            <p><strong>Plant:</strong> {plant_name}</p>
                            <p><strong>Status:</strong> No disease detected</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="info-box disease-box">
                            <h3>⚠️ Disease Detected</h3>
                            <p><strong>Plant:</strong> {plant_name}</p>
                            <p><strong>Disease:</strong> {disease_name}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Confidence metric
                    st.metric("Confidence Score", f"{confidence * 100:.2f}%")
                    st.progress(float(confidence))
                    
                    # Confidence interpretation
                    if confidence > 0.9:
                        st.success("🎯 Very high confidence")
                    elif confidence > 0.7:
                        st.info("👍 Good confidence")
                    else:
                        st.warning("⚠️ Low confidence - consider retaking the image")
                    
                except Exception as e:
                    st.error(f"❌ Error during prediction: {str(e)}")
                    st.exception(e)
                    return
        
        # Disease information and treatment
        if UTILS_AVAILABLE:
            disease_info = get_disease_info(disease_name)
            
            st.markdown("---")
            st.subheader("📋 Detailed Information")
            
            col3, col4 = st.columns(2)
            
            with col3:
                st.markdown("**🔍 Description:**")
                st.write(disease_info['description'])
            
            with col4:
                st.markdown("**💊 Treatment Recommendations:**")
                st.write(disease_info['treatment'])
        
        # Top predictions
        st.markdown("---")
        st.subheader("📊 Top 5 Predictions")
        
        top_5_idx = np.argsort(all_predictions)[-5:][::-1]
        
        for i, idx in enumerate(top_5_idx):
            label = CLASS_LABELS[idx]
            prob = all_predictions[idx]
            parts = label.split('___')
            display_plant = parts[0].replace('_', ' ')
            display_disease = parts[1].replace('_', ' ') if len(parts) > 1 else 'Unknown'
            
            col_a, col_b, col_c = st.columns([3, 2, 1])
            with col_a:
                st.write(f"**{i+1}. {display_plant}** - {display_disease}")
            with col_b:
                st.progress(float(prob))
            with col_c:
                st.write(f"{prob * 100:.1f}%")
    
    else:
        # Show welcome message when no image is uploaded
        st.info("👆 Please upload a plant leaf image to get started!")
        
        st.markdown("---")
        st.subheader("🌱 About This System")
        
        cols = st.columns(3)
        
        with cols[0]:
            st.markdown("""
            **🎯 Accuracy**
            
            State-of-the-art deep learning models trained on thousands of plant images.
            """)
        
        with cols[1]:
            st.markdown("""
            **⚡ Fast**
            
            Get instant results with real-time disease detection.
            """)
        
        with cols[2]:
            st.markdown("""
            **🌍 Accessible**
            
            Easy to use for farmers worldwide.
            """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🌿 <strong>Plant Disease Detection System</strong> 🌿</p>
        <p>Empowering sustainable agriculture through AI | © 2025</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
