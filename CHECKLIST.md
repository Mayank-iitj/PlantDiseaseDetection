# 🎯 Deployment Checklist

## ✅ Setup Complete - Follow This Guide

### Phase 1: Local Setup ⚙️

- [ ] **Step 1:** Open PowerShell in project directory
  ```powershell
  cd D:\PlantDiseaseDetection
  ```

- [ ] **Step 2:** Install Python dependencies
  ```powershell
  pip install -r requirements.txt
  ```

- [ ] **Step 3:** Download a pre-trained model
  - Visit: https://www.kaggle.com/datasets/gyanbardhan/vgg16
  - Download the `.h5` file
  - Create `models` folder if needed
  - Place file as `models\best_model.h5`

- [ ] **Step 4:** Run setup verification
  ```powershell
  python test_setup.py
  ```
  - Should see all ✅ green checkmarks

- [ ] **Step 5:** Test locally
  ```powershell
  # Option 1: Use launcher
  .\run.ps1
  
  # Option 2: Direct command
  streamlit run app.py
  ```

- [ ] **Step 6:** Upload a test image
  - Use a clear plant leaf image
  - Verify predictions are working
  - Check confidence scores

---

### Phase 2: Choose Deployment Platform 🚀

Pick ONE platform below:

#### Option A: Streamlit Cloud (Recommended for Beginners) ☁️

- [ ] Push code to GitHub
  ```powershell
  git add .
  git commit -m "Ready for deployment"
  git push origin main
  ```

- [ ] Upload model to cloud storage
  - Google Drive (recommended)
  - Dropbox
  - Kaggle Datasets
  - Get shareable link

- [ ] Update `app.py` to download model
  - Uncomment Google Drive download code
  - Add your file ID

- [ ] Deploy on Streamlit Cloud
  - Go to: https://share.streamlit.io
  - Click "New app"
  - Select your repository
  - Choose `app.py`
  - Click "Deploy"

- [ ] Test deployed app
  - Upload images
  - Verify predictions
  - Share the link!

---

#### Option B: Docker (Recommended for Self-Hosting) 🐳

- [ ] Install Docker Desktop
  - Download from: https://www.docker.com/products/docker-desktop

- [ ] Ensure model is in place
  ```powershell
  # Check model exists
  Test-Path models\best_model.h5
  ```

- [ ] Build Docker image
  ```powershell
  docker build -t plant-disease-detection .
  ```

- [ ] Run container
  ```powershell
  docker run -p 8501:8501 -v ${PWD}/models:/app/models plant-disease-detection
  ```
  
  **OR use Docker Compose:**
  ```powershell
  docker-compose up -d
  ```

- [ ] Access app at: http://localhost:8501

- [ ] Test and verify functionality

---

#### Option C: Heroku ☁️

- [ ] Install Heroku CLI
  ```powershell
  # Download from: https://devcenter.heroku.com/articles/heroku-cli
  ```

- [ ] Login to Heroku
  ```powershell
  heroku login
  ```

- [ ] Create Heroku app
  ```powershell
  heroku create your-plant-app-name
  ```

- [ ] Upload model to cloud storage
  - Get shareable URL
  - Update code to download model

- [ ] Deploy to Heroku
  ```powershell
  git push heroku main
  ```

- [ ] Open deployed app
  ```powershell
  heroku open
  ```

- [ ] Monitor logs
  ```powershell
  heroku logs --tail
  ```

---

#### Option D: AWS EC2 (Advanced) ⚡

- [ ] Launch EC2 instance (Ubuntu 20.04)

- [ ] SSH into instance

- [ ] Install dependencies
  ```bash
  sudo apt update
  sudo apt install python3-pip
  git clone https://github.com/yourusername/PlantDiseaseDetection.git
  cd PlantDiseaseDetection
  pip3 install -r requirements.txt
  ```

- [ ] Upload model file
  ```bash
  scp models/best_model.h5 ubuntu@your-ip:~/PlantDiseaseDetection/models/
  ```

- [ ] Run app
  ```bash
  streamlit run app.py --server.port 8501 --server.address 0.0.0.0
  ```

- [ ] Configure security group (allow port 8501)

- [ ] Access via: http://your-ec2-ip:8501

---

### Phase 3: Post-Deployment ✨

- [ ] **Test thoroughly**
  - Upload various plant images
  - Check all disease types
  - Verify confidence scores
  - Test on mobile devices

- [ ] **Monitor performance**
  - Check response times
  - Monitor memory usage
  - Review error logs

- [ ] **Share your app**
  - Get the public URL
  - Share with users/stakeholders
  - Gather feedback

- [ ] **Optional: Custom domain**
  - Purchase domain
  - Configure DNS
  - Add SSL certificate

---

### Phase 4: Maintenance 🔧

- [ ] **Regular updates**
  - Update dependencies monthly
  - Retrain model with new data
  - Add new features

- [ ] **Backup**
  - Backup trained models
  - Version control code
  - Document changes

- [ ] **Monitor usage**
  - Track user metrics
  - Collect feedback
  - Fix reported issues

---

## 📊 Progress Tracker

| Task | Status | Notes |
|------|--------|-------|
| Install dependencies | ⬜ |  |
| Download model | ⬜ |  |
| Test locally | ⬜ |  |
| Choose platform | ⬜ | Platform: _______ |
| Deploy | ⬜ |  |
| Test deployment | ⬜ |  |
| Share URL | ⬜ | URL: _______ |

---

## 🆘 Need Help?

**Issue:** Dependencies won't install
- **Solution:** Try `pip install -r requirements.txt --upgrade`

**Issue:** Model not found
- **Solution:** Verify file is at `models\best_model.h5` exactly

**Issue:** Can't access deployed app
- **Solution:** Check firewall/security group settings

**Issue:** Predictions are wrong
- **Solution:** Verify model file isn't corrupted, re-download if needed

**Issue:** Out of memory
- **Solution:** Use smaller images or deploy to platform with more RAM

---

## 📚 Quick Reference

### Essential Commands

```powershell
# Test setup
python test_setup.py

# Run basic app
streamlit run app.py

# Run enhanced app
streamlit run app_enhanced.py

# Run with custom port
streamlit run app.py --server.port 8502

# Docker build
docker build -t plant-disease .

# Docker run
docker-compose up

# Git push
git add .
git commit -m "Update"
git push
```

### Important Files

- `app.py` - Basic Streamlit app
- `app_enhanced.py` - Enhanced app with features
- `models/best_model.h5` - Your trained model
- `requirements.txt` - Python dependencies
- `.streamlit/config.toml` - Streamlit settings

### Important Links

- **Model Downloads:** https://www.kaggle.com/datasets/gyanbardhan/vgg16
- **Streamlit Cloud:** https://share.streamlit.io
- **Docker Hub:** https://hub.docker.com
- **Heroku:** https://dashboard.heroku.com

---

## ✅ Final Checklist

Before going live:

- [ ] Code is tested and working locally
- [ ] Model file is accessible
- [ ] All dependencies are installed
- [ ] Configuration is correct
- [ ] Environment variables are set
- [ ] Documentation is updated
- [ ] Deployment platform is chosen
- [ ] App is deployed successfully
- [ ] Testing on deployment is complete
- [ ] URL is shared with users
- [ ] Monitoring is set up

---

**🎉 Congratulations on deploying your Plant Disease Detection app!**

*Made with 🌿 for sustainable agriculture*
