import streamlit as st
import tensorflow as tf
from tensorflow import keras
from PIL import Image
import numpy as np
import os
import gdown

# Page configuration
st.set_page_config(
    page_title="Plant Disease Detection",
    page_icon="🌿",
    layout="wide"
)

# Class labels for plant diseases
CLASS_LABELS = [
    'Apple___Apple_scab',
    'Apple___Black_rot',
    'Apple___Cedar_apple_rust',
    'Apple___healthy',
    'Blueberry___healthy',
    'Cherry_(including_sour)___Powdery_mildew',
    'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight',
    'Corn_(maize)___healthy',
    'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)',
    'Peach___Bacterial_spot',
    'Peach___healthy',
    'Pepper,_bell___Bacterial_spot',
    'Pepper,_bell___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Raspberry___healthy',
    'Soybean___healthy',
    'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch',
    'Strawberry___healthy',
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

@st.cache_resource
def load_model():
    """Load the trained model"""
    model_path = 'models/best_model.h5'
    
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # If model doesn't exist locally, provide instructions
    if not os.path.exists(model_path):
        st.warning("⚠️ Model file not found. Please place your trained model at `models/best_model.h5`")
        st.info("You can download a pre-trained model from the Kaggle links provided in the README")
        return None
    
    try:
        model = keras.models.load_model(model_path)
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

def preprocess_image(image, target_size=(224, 224)):
    """Preprocess the uploaded image"""
    # Convert to RGB if necessary
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize image
    image = image.resize(target_size)
    
    # Convert to array and normalize
    img_array = np.array(image)
    img_array = img_array.astype('float32') / 255.0
    
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

def predict_disease(model, image):
    """Make prediction on the image"""
    processed_image = preprocess_image(image)
    predictions = model.predict(processed_image)
    predicted_class = np.argmax(predictions[0])
    confidence = predictions[0][predicted_class]
    
    return CLASS_LABELS[predicted_class], confidence, predictions[0]

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
        This system uses state-of-the-art CNN architectures including:
        - VGG16/VGG19
        - ResNet
        - DenseNet
        - EfficientNet
        - ConvNextLarge
        - AlexNet
        """)
        
        st.header("Instructions")
        st.markdown("""
        1. Upload a clear image of a plant leaf
        2. Wait for the model to process
        3. View the prediction and confidence score
        4. Check top predictions for more details
        """)
    
    # Load model
    model = load_model()
    
    if model is None:
        st.error("❌ Cannot proceed without a model. Please add your trained model to continue.")
        st.markdown("""
        ### How to add your model:
        1. Create a `models` folder in the project directory
        2. Place your trained model file as `models/best_model.h5`
        3. Refresh this page
        
        You can download pre-trained models from:
        - [VGG16 Model](https://www.kaggle.com/datasets/gyanbardhan/vgg16)
        - [VGG19 Model](https://www.kaggle.com/datasets/clay108/vgg19-123)
        - [AlexNet Model](https://www.kaggle.com/datasets/gyanbardhan/alexnet123)
        """)
        return
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a plant leaf image...",
        type=['jpg', 'jpeg', 'png'],
        help="Upload a clear image of a plant leaf for disease detection"
    )
    
    if uploaded_file is not None:
        # Create two columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Uploaded Image")
            image = Image.open(uploaded_file)
            st.image(image, use_container_width=True)
        
        with col2:
            st.subheader("Prediction Results")
            
            with st.spinner("Analyzing image..."):
                try:
                    # Make prediction
                    predicted_label, confidence, all_predictions = predict_disease(model, image)
                    
                    # Parse the prediction
                    parts = predicted_label.split('___')
                    plant_name = parts[0].replace('_', ' ')
                    disease_name = parts[1].replace('_', ' ') if len(parts) > 1 else 'Unknown'
                    
                    # Display results
                    if disease_name.lower() == 'healthy':
                        st.success(f"✅ **{plant_name}** - Healthy!")
                    else:
                        st.warning(f"⚠️ **{plant_name}** - {disease_name}")
                    
                    st.metric("Confidence", f"{confidence * 100:.2f}%")
                    
                    # Show progress bar for confidence
                    st.progress(float(confidence))
                    
                    # Show top 5 predictions
                    st.subheader("Top 5 Predictions")
                    top_5_idx = np.argsort(all_predictions)[-5:][::-1]
                    
                    for idx in top_5_idx:
                        label = CLASS_LABELS[idx]
                        prob = all_predictions[idx]
                        parts = label.split('___')
                        display_name = f"{parts[0]} - {parts[1]}" if len(parts) > 1 else label
                        st.write(f"**{display_name}**: {prob * 100:.2f}%")
                    
                except Exception as e:
                    st.error(f"Error during prediction: {str(e)}")
                    st.exception(e)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <p>Developed for sustainable agriculture and food security 🌱</p>
        <p><a href='https://huggingface.co/spaces/gyanbardhan123/PlantDiseaseDetection'>Visit our Hugging Face Space</a></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
