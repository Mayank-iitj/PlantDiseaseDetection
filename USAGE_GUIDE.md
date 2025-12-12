# 🌿 Plant Disease Detection - Usage Guide

## Overview
This application uses a VGG19-based deep learning model to classify plant leaves as **Healthy** or **Diseased**. The model was trained using transfer learning and achieves high accuracy in binary classification.

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- All dependencies from requirements.txt installed

### Running the Application Locally

1. **Navigate to the project directory:**
   ```powershell
   cd d:\PlantDiseaseDetection
   ```

2. **Run the Streamlit app:**
   ```powershell
   python -m streamlit run app.py
   ```

3. **Open your browser:**
   - The app will automatically open at http://localhost:8501
   - Or manually navigate to the URL shown in the terminal

## 📖 How to Use the Application

### Step 1: Upload an Image
1. Click on the **"Choose a plant leaf image..."** button
2. Select a clear image of a plant leaf from your computer
3. Supported formats: JPG, JPEG, PNG
4. The image will be displayed in the left column

### Step 2: Wait for Analysis
- The model will automatically process the image
- Processing typically takes less than 1 second
- You'll see a loading spinner during analysis

### Step 3: Review Results
The application displays:
- **Classification**: Healthy or Diseased
- **Confidence Score**: How certain the model is (0-100%)
- **Prediction Details**: Probability breakdown
- **Visual Chart**: Bar chart showing probabilities for both classes

## 🎯 Understanding the Results

### Classification Output
- **✅ Healthy**: The leaf shows no signs of disease
- **⚠️ Diseased**: The leaf shows signs of disease

### Confidence Score
- **90-100%**: Very high confidence
- **70-90%**: High confidence
- **50-70%**: Moderate confidence
- **Below 50%**: Low confidence (review image quality)

### Tips for Best Results
1. **Use clear, well-lit images**
2. **Focus on the leaf surface**
3. **Avoid blurry or dark images**
4. **Ensure the leaf fills most of the frame**
5. **Use images with good contrast**

## 🛠️ Technical Details

### Model Information
- **Architecture**: VGG19 with Transfer Learning
- **Input Size**: 150x150 pixels (RGB)
- **Output**: Binary classification (Sigmoid activation)
- **Framework**: TensorFlow/Keras
- **Model Size**: ~134 MB

### Image Preprocessing
The application automatically:
1. Converts images to RGB format
2. Resizes to 150x150 pixels
3. Normalizes pixel values to [0, 1]
4. Adds batch dimension for prediction

## 🔧 Troubleshooting

### Model Not Found
If you see "Model file not found":
1. Ensure est_model.h5 is in the models/ directory
2. Check file permissions
3. Verify the file is not corrupted

### Slow Performance
If predictions are slow:
1. Close other resource-intensive applications
2. Use smaller image files
3. Ensure you have adequate RAM (8GB+ recommended)

### Installation Issues
If packages fail to install:
```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

## 📊 Model Performance

### Training Details
- The model uses VGG19 pre-trained on ImageNet
- Custom dense layers added for binary classification
- Dropout layer (0.5) to prevent overfitting
- Trained on plant disease dataset

### Expected Accuracy
- The binary classification model achieves high accuracy
- Performance depends on image quality and lighting
- Best results with clear, focused leaf images

## 🌐 Deployment Options

### Local Deployment
Already running! Just use:
```powershell
python -m streamlit run app.py
```

### Cloud Deployment (Streamlit Cloud)
1. Push code to GitHub
2. Go to share.streamlit.io
3. Connect your repository
4. Deploy!

### Heroku Deployment
The project includes:
- Procfile for Heroku
- setup.sh for configuration
- untime.txt for Python version

## 📝 Additional Resources

### Files in This Project
- pp.py - Main application file
- model_loader.py - Model loading utilities
- models/best_model.h5 - Trained model weights
- equirements.txt - Python dependencies
- Procfile - Heroku configuration
- setup.sh - Streamlit configuration

### Documentation
- See README.md for project overview
- See MODEL_SETUP.md for model deployment details
- See DEPLOYMENT_SUMMARY.md for deployment guide

## 🤝 Support

For issues or questions:
1. Check this usage guide
2. Review the README.md
3. Check the repository issues page
4. Review the model setup documentation

## 📄 License

This project is part of a plant disease detection research initiative.

---

**Last Updated**: November 23, 2025

**Model Version**: VGG19 Binary Classifier v1.0

**Supported by**: TensorFlow 2.20.0, Streamlit 1.51.0
