# Plant Disease Detection - Deployment Guide

## 🚀 Quick Start

### Local Development

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Add Your Model**
   - Place your trained model file in the `models/` directory
   - Rename it to `best_model.h5`

3. **Run the Application**
```bash
streamlit run app.py
```

4. **Open Browser**
   - Navigate to `http://localhost:8501`

## 📦 Deployment Options

### 1. Streamlit Cloud (Recommended)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy!

**Note:** Upload your model file to:
- Google Drive (share publicly)
- Kaggle Datasets
- GitHub LFS (for files < 100MB)

Update the `load_model()` function in `app.py` to download from your chosen location.

### 2. Docker Deployment

**Build Image:**
```bash
docker build -t plant-disease-detection .
```

**Run Container:**
```bash
docker run -p 8501:8501 -v $(pwd)/models:/app/models plant-disease-detection
```

**Or use Docker Compose:**
```bash
docker-compose up -d
```

### 3. Heroku Deployment

1. **Install Heroku CLI**
```bash
# Windows
choco install heroku-cli

# Or download from heroku.com
```

2. **Login and Create App**
```bash
heroku login
heroku create your-app-name
```

3. **Deploy**
```bash
git add .
git commit -m "Initial deployment"
git push heroku main
```

4. **Set Environment Variables (if needed)**
```bash
heroku config:set MODEL_URL=your_model_url
```

### 4. AWS EC2 Deployment

1. **Launch EC2 Instance** (Ubuntu 20.04 LTS)

2. **SSH into Instance**
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

3. **Install Dependencies**
```bash
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements.txt
```

4. **Run with systemd or supervisor**
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### 5. Google Cloud Platform (Cloud Run)

1. **Build and Push to Container Registry**
```bash
gcloud builds submit --tag gcr.io/PROJECT-ID/plant-disease
```

2. **Deploy to Cloud Run**
```bash
gcloud run deploy --image gcr.io/PROJECT-ID/plant-disease --platform managed
```

### 6. Azure Web App

1. **Create Web App**
```bash
az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name myapp --runtime "PYTHON|3.9"
```

2. **Deploy**
```bash
az webapp up --name myapp
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file for local development:
```env
MODEL_PATH=models/best_model.h5
MAX_UPLOAD_SIZE=200
DEBUG=False
```

### Streamlit Configuration

The `.streamlit/config.toml` file contains:
- Theme settings
- Server configuration
- Upload limits

Modify as needed for your deployment.

## 📊 Model Management

### Downloading Models Automatically

Update `app.py` to download models from cloud storage:

```python
import gdown

@st.cache_resource
def load_model():
    model_path = 'models/best_model.h5'
    
    if not os.path.exists(model_path):
        # Google Drive download
        file_id = 'YOUR_GOOGLE_DRIVE_FILE_ID'
        url = f'https://drive.google.com/uc?id={file_id}'
        gdown.download(url, model_path, quiet=False)
    
    return keras.models.load_model(model_path)
```

### Model Files

Supported formats:
- `.h5` (HDF5 format)
- `.keras` (Keras 3.0+)
- SavedModel format (directory)

## 🔒 Security Best Practices

1. **Never commit model files or API keys to Git**
2. Use environment variables for sensitive data
3. Enable XSRF protection (already configured)
4. Set appropriate upload size limits
5. Validate uploaded files before processing

## 📈 Performance Optimization

1. **Use caching:**
   - `@st.cache_resource` for model loading
   - `@st.cache_data` for data processing

2. **Optimize model:**
   - Use quantization for smaller model size
   - Convert to TensorFlow Lite for mobile

3. **Enable compression:**
   - Configure server compression in config.toml

## 🐛 Troubleshooting

### Common Issues

**1. Model not loading:**
- Check file path
- Verify TensorFlow version compatibility
- Ensure model file is not corrupted

**2. Out of memory:**
- Reduce batch size
- Use smaller input image size
- Enable model quantization

**3. Slow predictions:**
- Use GPU if available
- Implement model caching
- Reduce image resolution

## 📝 Testing

Test the application locally:
```bash
# Run unit tests (create test files as needed)
python -m pytest tests/

# Test with sample images
python test_predictions.py
```

## 🔄 CI/CD Pipeline

Example GitHub Actions workflow (`.github/workflows/deploy.yml`):

```yaml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Streamlit
        run: echo "Auto-deploy configured in Streamlit Cloud"
```

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [TensorFlow Deployment Guide](https://www.tensorflow.org/tfx/guide/serving)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## 🆘 Support

For issues and questions:
- Check the [GitHub Issues](https://github.com/Gyanbardhan/PlantDiseaseDetection/issues)
- Review the main README.md
- Contact: [Your Contact Info]

---
**Happy Deploying! 🌿**
