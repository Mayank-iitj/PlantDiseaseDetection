# 🧠 Model Setup for Deployment

## Problem
The trained model file (`models/best_model.h5` - 128MB) cannot be pushed to GitHub because:
- It's too large for regular git
- It's excluded in `.gitignore`
- GitHub has 100MB file size limit

## ✅ Solutions for Streamlit Cloud Deployment

### **Option 1: Google Drive** (Recommended - Easiest)

1. **Upload your model to Google Drive**
   - Go to https://drive.google.com
   - Upload `models/best_model.h5`

2. **Make it publicly accessible**
   - Right-click the file → Share
   - Change to "Anyone with the link can view"
   - Copy the link (format: `https://drive.google.com/file/d/FILE_ID/view?usp=sharing`)

3. **Get the File ID**
   - From the URL above, extract the `FILE_ID` part
   - Example: If URL is `https://drive.google.com/file/d/1ABC123xyz/view?usp=sharing`
   - File ID is: `1ABC123xyz`

4. **Add to Streamlit Cloud Secrets**
   - Go to your app on Streamlit Cloud
   - Click "Settings" → "Secrets"
   - Add:
   ```toml
   [model]
   google_drive_id = "YOUR_FILE_ID_HERE"
   ```

5. **Update the app code** (I'll do this for you)

---

### **Option 2: Hugging Face Hub** (Recommended - Best for ML)

1. **Create Hugging Face account**
   - Go to https://huggingface.co
   - Sign up for free

2. **Upload your model**
   ```bash
   pip install huggingface_hub
   
   python -c "
   from huggingface_hub import HfApi
   api = HfApi()
   api.upload_file(
       path_or_fileobj='models/best_model.h5',
       path_in_repo='best_model.h5',
       repo_id='YOUR_USERNAME/plant-disease-model',
       repo_type='model'
   )
   "
   ```

3. **Model will be at**: `https://huggingface.co/YOUR_USERNAME/plant-disease-model`

4. **Add to Streamlit Secrets**:
   ```toml
   [model]
   huggingface_repo = "YOUR_USERNAME/plant-disease-model"
   huggingface_filename = "best_model.h5"
   ```

---

### **Option 3: GitHub LFS** (For developers)

1. **Install Git LFS**
   ```bash
   git lfs install
   ```

2. **Track .h5 files**
   ```bash
   git lfs track "*.h5"
   git add .gitattributes
   ```

3. **Add and commit model**
   ```bash
   git add models/best_model.h5
   git commit -m "Add model file with LFS"
   git push
   ```

**Note**: GitHub LFS has bandwidth limits (1GB/month free)

---

### **Option 4: AWS S3 / Azure Blob** (For production)

1. Upload model to cloud storage
2. Generate public URL or use access keys
3. Add credentials to Streamlit secrets
4. Download in app using boto3 or azure-storage-blob

---

## 🚀 Quick Start (Google Drive Method)

**Step 1**: Upload your model to Google Drive and get the File ID

**Step 2**: In Streamlit Cloud, add this to Secrets:
```toml
[model]
google_drive_id = "1ABC123xyz"  # Your actual file ID
```

**Step 3**: Reboot your Streamlit app

**Step 4**: The app will automatically download the model on first run!

---

## 📝 For Local Development

Just keep your model at `D:\PlantDiseaseDetection\models\best_model.h5`

The app will use the local file and skip downloading.

---

## ❓ Which Option Should I Choose?

| Option | Pros | Cons | Best For |
|--------|------|------|----------|
| **Google Drive** | ✅ Easy<br>✅ Free<br>✅ Fast setup | ❌ Download speed limits | Quick deployment |
| **Hugging Face** | ✅ Made for ML<br>✅ Version control<br>✅ Free | ❌ Requires account | Production ML apps |
| **GitHub LFS** | ✅ Integrated with git<br>✅ Version control | ❌ Bandwidth limits<br>❌ Complex setup | Open source projects |
| **AWS/Azure** | ✅ Production-grade<br>✅ Fast<br>✅ Scalable | ❌ Costs money<br>❌ Complex setup | Enterprise apps |

**My Recommendation**: Start with **Google Drive** (easiest), move to **Hugging Face** for production.

---

## 🆘 Need Help?

1. Upload model to Google Drive
2. Share the File ID with me
3. I'll update the code to download it automatically!
