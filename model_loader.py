"""
Model loader utility with support for cloud storage
"""
import os
import streamlit as st
from tensorflow import keras


def download_from_google_drive(file_id, destination):
    """Download file from Google Drive using gdown"""
    try:
        import gdown
        url = f'https://drive.google.com/uc?id={file_id}'
        gdown.download(url, destination, quiet=False)
        return True
    except Exception as e:
        st.error(f"Error downloading from Google Drive: {str(e)}")
        return False


def download_from_huggingface(repo_id, filename, destination):
    """Download model from Hugging Face Hub"""
    try:
        from huggingface_hub import hf_hub_download
        downloaded_path = hf_hub_download(repo_id=repo_id, filename=filename)
        # Copy to destination
        import shutil
        shutil.copy(downloaded_path, destination)
        return True
    except Exception as e:
        st.error(f"Error downloading from Hugging Face: {str(e)}")
        return False


@st.cache_resource
def load_model_with_download():
    """
    Load model with automatic download from cloud storage
    Supports: Google Drive, Hugging Face, local file
    """
    model_path = 'models/best_model.h5'
    os.makedirs('models', exist_ok=True)
    
    # If model exists locally, load it
    if os.path.exists(model_path):
        try:
            st.success("✅ Loading model from local storage...")
            model = keras.models.load_model(model_path)
            st.success(f"✅ Model loaded successfully! ({os.path.getsize(model_path) / (1024*1024):.2f} MB)")
            return model
        except Exception as e:
            st.error(f"Error loading local model: {str(e)}")
            return None
    
    # Model doesn't exist, try to download
    st.info("📥 Model not found locally. Attempting download from cloud storage...")
    
    # Try to get credentials from Streamlit secrets
    try:
        secrets = st.secrets.get("model", {})
        
        # Option 1: Google Drive
        if "google_drive_id" in secrets:
            file_id = secrets["google_drive_id"]
            st.info(f"📥 Downloading from Google Drive (ID: {file_id[:8]}...)...")
            
            if download_from_google_drive(file_id, model_path):
                st.success("✅ Model downloaded successfully!")
                model = keras.models.load_model(model_path)
                return model
        
        # Option 2: Hugging Face
        elif "huggingface_repo" in secrets:
            repo_id = secrets["huggingface_repo"]
            filename = secrets.get("huggingface_filename", "best_model.h5")
            st.info(f"📥 Downloading from Hugging Face ({repo_id})...")
            
            if download_from_huggingface(repo_id, filename, model_path):
                st.success("✅ Model downloaded successfully!")
                model = keras.models.load_model(model_path)
                return model
        
        else:
            st.warning("⚠️ No model download configuration found in secrets.")
            show_setup_instructions()
            return None
            
    except Exception as e:
        st.warning(f"⚠️ Could not access secrets: {str(e)}")
        show_setup_instructions()
        return None


def show_setup_instructions():
    """Display setup instructions for model deployment"""
    st.markdown("""
    ### 🔧 Model Setup Required
    
    Your app is deployed but the model file is missing. Here's how to fix it:
    
    #### **Quick Fix: Google Drive** (Recommended)
    
    1. **Upload your model** (`best_model.h5`) to Google Drive
    2. **Share it publicly**: Right-click → Share → "Anyone with link can view"
    3. **Get the File ID** from the share URL:
       ```
       https://drive.google.com/file/d/FILE_ID_HERE/view?usp=sharing
       ```
    4. **Add to Streamlit Cloud**:
       - Go to your app settings
       - Click "Secrets"
       - Add this:
       ```toml
       [model]
       google_drive_id = "YOUR_FILE_ID_HERE"
       ```
    5. **Reboot your app** - it will auto-download the model!
    
    ---
    
    #### Alternative: Hugging Face
    
    ```toml
    [model]
    huggingface_repo = "your-username/plant-disease-model"
    huggingface_filename = "best_model.h5"
    ```
    
    ---
    
    📖 **Full guide**: See `MODEL_SETUP.md` in the repository
    
    💬 **Need help?** Check the repository README for detailed instructions
    """)
