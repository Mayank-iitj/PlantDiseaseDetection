# Plant Disease Detection - Run Script
# This script helps you start the application

Write-Host "=" -NoNewline -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Green
Write-Host "  Plant Disease Detection - Application Launcher" -ForegroundColor Green
Write-Host "=" * 61 -ForegroundColor Green
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found! Please install Python 3.9+" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Checking setup..." -ForegroundColor Cyan

# Run setup test
python test_setup.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=" * 61 -ForegroundColor Green
    Write-Host "  Choose Application Version" -ForegroundColor Green
    Write-Host "=" * 61 -ForegroundColor Green
    Write-Host ""
    Write-Host "1. Basic App (app.py) - Simple and fast" -ForegroundColor Yellow
    Write-Host "2. Enhanced App (app_enhanced.py) - Full features" -ForegroundColor Yellow
    Write-Host "3. Exit" -ForegroundColor Gray
    Write-Host ""
    
    $choice = Read-Host "Enter your choice (1-3)"
    
    switch ($choice) {
        "1" {
            Write-Host ""
            Write-Host "🚀 Starting Basic App..." -ForegroundColor Cyan
            Write-Host ""
            streamlit run app.py
        }
        "2" {
            Write-Host ""
            Write-Host "🚀 Starting Enhanced App..." -ForegroundColor Cyan
            Write-Host ""
            streamlit run app_enhanced.py
        }
        "3" {
            Write-Host "Goodbye! 👋" -ForegroundColor Cyan
            exit 0
        }
        default {
            Write-Host "Invalid choice. Exiting." -ForegroundColor Red
            exit 1
        }
    }
} else {
    Write-Host ""
    Write-Host "⚠️  Setup check failed. Please fix the issues above." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Common fixes:" -ForegroundColor Cyan
    Write-Host "  1. Install dependencies: pip install -r requirements.txt" -ForegroundColor White
    Write-Host "  2. Download model from Kaggle and place in models/best_model.h5" -ForegroundColor White
    Write-Host ""
    
    $install = Read-Host "Would you like to install dependencies now? (y/n)"
    
    if ($install -eq "y" -or $install -eq "Y") {
        Write-Host ""
        Write-Host "Installing dependencies..." -ForegroundColor Cyan
        pip install -r requirements.txt
        
        Write-Host ""
        Write-Host "✅ Dependencies installed!" -ForegroundColor Green
        Write-Host "⚠️  Don't forget to download the model file!" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Download from:" -ForegroundColor Cyan
        Write-Host "  https://www.kaggle.com/datasets/gyanbardhan/vgg16" -ForegroundColor White
        Write-Host ""
    }
}
