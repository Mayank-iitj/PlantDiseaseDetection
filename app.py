import streamlit as st
import tensorflow as tf
from tensorflow import keras
from PIL import Image
import numpy as np
import os
from io import BytesIO
try:
    import cv2  # Fallback decoder for images PIL cannot parse
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

# Page configuration
st.set_page_config(
    page_title="Plant Disease Detection",
    page_icon="🌿",
    layout="wide"
)

# Binary classification model - detects healthy vs diseased plants

@st.cache_resource
def load_model():
    """Load the trained model from local storage"""
    model_path = 'models/best_model.h5'
    
    if not os.path.exists(model_path):
        st.error(f"❌ Model file not found at `{model_path}`")
        st.info("Please ensure the model file exists in the models directory.")
        return None
    
    try:
        model = keras.models.load_model(model_path)
        model_size_mb = os.path.getsize(model_path) / (1024 * 1024)
        st.success(f"✅ Model loaded successfully ({model_size_mb:.1f} MB)")
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

def preprocess_image(image, target_size=(150, 150)):
    """Preprocess the uploaded image"""
    # Convert to RGB if necessary
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize image to match model input (150x150)
    image = image.resize(target_size)
    
    # Convert to array and normalize
    img_array = np.array(image)
    img_array = img_array.astype('float32') / 255.0
    
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

def predict_disease(model, image):
    """Make prediction on the image - Binary classification (Healthy vs Diseased)"""
    processed_image = preprocess_image(image)
    predictions = model.predict(processed_image)
    
    # Binary classification: output is probability of being diseased
    disease_probability = float(predictions[0][0])
    
    # Threshold at 0.5 for binary classification
    if disease_probability > 0.5:
        predicted_class = "Diseased"
        confidence = disease_probability
    else:
        predicted_class = "Healthy"
        confidence = 1.0 - disease_probability
    
    return predicted_class, confidence, disease_probability

def main():
    # Header
    st.title("🌿 Plant Disease Detection System")
    st.markdown("""
    This application uses deep learning to detect diseases in plant leaves.
    Upload an image of a plant leaf to get started!
    """)
    
    # Sidebar
    with st.sidebar:
        st.header("About")
        st.info("""
        This system uses a VGG19-based CNN model for binary classification:
        - **Healthy**: Plant leaf is healthy
        - **Diseased**: Plant leaf shows signs of disease
        
        Model Details:
        - Architecture: VGG19 (Transfer Learning)
        - Input: 150x150 RGB images
        - Output: Binary classification
        """)
        
        st.header("Instructions")
        st.markdown("""
        1. Upload a clear image of a plant leaf
        2. Wait for the model to process (usually < 1 second)
        3. View the prediction: Healthy or Diseased
        4. Check the confidence score
        5. Review the probability distribution
        """)
        
        st.header("Model Information")
        st.markdown("""
        - **Model Type**: VGG19 Transfer Learning
        - **Input Size**: 150x150 pixels
        - **Classes**: Binary (Healthy/Diseased)
        - **Framework**: TensorFlow/Keras
        """)
    
    # Load model
    model = load_model()
    
    if model is None:
        st.stop()
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a plant leaf image...",
        type=['jpg', 'jpeg', 'png'],
        help="Upload a clear image of a plant leaf for disease detection"
    )
    
    if uploaded_file is not None:
        # Create two columns
        col1, col2 = st.columns(2)

        # Robust image loader helper defined inline for clarity
        def load_uploaded_image(file_obj):
            # Reset pointer and read bytes once
            try:
                file_obj.seek(0)
            except Exception:
                pass
            raw_bytes = file_obj.read()
            if not raw_bytes:
                raise ValueError("Uploaded file is empty")

            # Skip signature validation - just try to decode
            # Many valid images have non-standard headers but decode fine

            # First attempt: PIL
            try:
                img = Image.open(BytesIO(raw_bytes))
                img.load()  # Force loading to catch errors early
                return img
            except Exception as pil_err:
                # Fallback: OpenCV
                try:
                    np_arr = np.frombuffer(raw_bytes, np.uint8)
                    cv_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                    if cv_img is None:
                        raise ValueError("OpenCV failed to decode image")
                    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
                    return Image.fromarray(cv_img)
                except Exception as cv_err:
                    raise ValueError(f"PIL error: {pil_err}; OpenCV error: {cv_err}")

        with col1:
            st.subheader("Uploaded Image")
            try:
                image = load_uploaded_image(uploaded_file)
                st.image(image, use_container_width=True)
            except Exception as e:
                st.error(f"Error loading image: {e}")
                st.error(f"File type: {uploaded_file.type}, Size: {uploaded_file.size} bytes")
                # Show first 16 bytes for debugging (hex)
                try:
                    uploaded_file.seek(0)
                    dbg_bytes = uploaded_file.read(16)
                    st.code(dbg_bytes.hex(' '), language='text')
                except Exception:
                    pass
                st.info("If this is a real PNG/JPEG, ensure it is not corrupted. Try re-saving the file.")
                st.stop()

        with col2:
            st.subheader("Prediction Results")
            with st.spinner("Analyzing image..."):
                try:
                    predicted_label, confidence, disease_prob = predict_disease(model, image)
                    if predicted_label.lower() == 'healthy':
                        st.success("✅ **Plant is Healthy!**")
                    else:
                        st.warning("⚠️ **Plant Disease Detected!**")
                    st.metric("Classification", predicted_label)
                    st.metric("Confidence", f"{confidence * 100:.2f}%")
                    st.progress(float(confidence))
                    st.subheader("Prediction Details")
                    st.write(f"**Disease Probability**: {disease_prob * 100:.2f}%")
                    st.write(f"**Healthy Probability**: {(1 - disease_prob) * 100:.2f}%")
                    import pandas as pd
                    chart_data = pd.DataFrame({
                        'Category': ['Healthy', 'Diseased'],
                        'Probability': [(1 - disease_prob) * 100, disease_prob * 100]
                    })
                    st.bar_chart(chart_data.set_index('Category'))
                except Exception as e:
                    st.error(f"Error during prediction: {e}")
                    st.exception(e)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <p>Developed for sustainable agriculture and food security 🌱</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
