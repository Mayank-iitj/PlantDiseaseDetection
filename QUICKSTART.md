# Plant Disease Detection - Quick Start Guide

## 🚀 Getting Started

### Step 1: Install Dependencies

```bash
# Install basic requirements
pip install -r requirements.txt

# Or install with OpenCV for better preprocessing
pip install -r requirements_full.txt
```

### Step 2: Download Model

You need to download a pre-trained model and place it in the `models/` directory:

1. Choose a model from:
   - [VGG16 Model](https://www.kaggle.com/datasets/gyanbardhan/vgg16) - Recommended
   - [VGG19 Model](https://www.kaggle.com/datasets/clay108/vgg19-123)
   - [AlexNet Model](https://www.kaggle.com/datasets/gyanbardhan/alexnet123)

2. Download the `.h5` file

3. Place it as: `models/best_model.h5`

### Step 3: Test Setup

```bash
python test_setup.py
```

This will verify:
- ✅ All dependencies are installed
- ✅ Model file is in place
- ✅ Directory structure is correct

### Step 4: Run Application

```bash
# Basic app
streamlit run app.py

# Enhanced app with more features
streamlit run app_enhanced.py
```

The application will open in your browser at `http://localhost:8501`

## 📱 Using the Application

1. **Upload Image**: Click "Browse files" and select a plant leaf image
2. **Wait for Analysis**: The model will process the image
3. **View Results**: See the predicted disease and confidence score
4. **Read Recommendations**: Get treatment suggestions (in enhanced version)

## 🐳 Docker Deployment

```bash
# Build image
docker build -t plant-disease-detection .

# Run container
docker run -p 8501:8501 -v $(pwd)/models:/app/models plant-disease-detection

# Or use Docker Compose
docker-compose up
```

## 🌐 Cloud Deployment

### Streamlit Cloud (Easiest)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Add secrets for model URL if needed
5. Deploy!

### Heroku

```bash
heroku create your-app-name
git push heroku main
```

### Other Platforms

See `README_DEPLOYMENT.md` for detailed instructions on:
- AWS EC2
- Google Cloud Run
- Azure Web Apps

## 🔧 Troubleshooting

### Model Not Loading

**Problem**: "Model file not found" error

**Solution**:
```bash
# Verify model exists
ls -la models/

# Should see: best_model.h5
```

### Import Errors

**Problem**: Missing package errors

**Solution**:
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Memory Issues

**Problem**: Out of memory during prediction

**Solution**:
- Use smaller images (resize before upload)
- Reduce batch size in code
- Use a smaller model

### Slow Predictions

**Problem**: Takes too long to predict

**Solution**:
- Ensure TensorFlow is using GPU if available
- Use model quantization
- Reduce image resolution

## 📝 File Structure

```
PlantDiseaseDetection/
├── app.py                  # Main Streamlit app
├── app_enhanced.py         # Enhanced version with more features
├── utils.py               # Helper functions
├── requirements.txt       # Basic dependencies
├── requirements_full.txt  # Full dependencies with OpenCV
├── test_setup.py          # Setup verification script
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── Procfile              # Heroku deployment
├── setup.sh              # Heroku setup script
├── runtime.txt           # Python version
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── models/
│   ├── .gitkeep
│   └── best_model.h5     # Your trained model (download separately)
├── README.md             # Original README
├── README_DEPLOYMENT.md  # Detailed deployment guide
└── QUICKSTART.md         # This file
```

## 🎯 Supported Plants & Diseases

The model can detect 38 different plant-disease combinations including:

**Plants:**
- Apple, Blueberry, Cherry
- Corn, Grape, Orange
- Peach, Pepper, Potato
- Raspberry, Soybean, Squash
- Strawberry, Tomato

**Diseases:**
- Fungal: Scab, Black rot, Rust, Blight, Mildew
- Bacterial: Bacterial spot
- Viral: Mosaic virus, Yellow leaf curl
- Healthy (no disease)

## 💡 Tips for Best Results

1. **Image Quality**: Use clear, well-lit photos
2. **Focus**: Ensure the leaf fills most of the frame
3. **Background**: Plain background works best
4. **Lighting**: Natural, even lighting is ideal
5. **Angle**: Take photo straight-on, not at an angle

## 🆘 Getting Help

- **Issues**: [GitHub Issues](https://github.com/Gyanbardhan/PlantDiseaseDetection/issues)
- **Documentation**: See `Documentation.pdf`
- **Demo**: [Hugging Face Space](https://huggingface.co/spaces/gyanbardhan123/PlantDiseaseDetection)

## 📚 Next Steps

- Explore the Jupyter notebooks to see model training
- Try different model architectures
- Fine-tune on your own dataset
- Deploy to production

---

**Happy detecting! 🌿**
