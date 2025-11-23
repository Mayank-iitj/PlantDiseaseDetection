#!/bin/bash
# Plant Disease Detection - Run Script (Linux/Mac)

echo "=============================================================="
echo "  Plant Disease Detection - Application Launcher"
echo "=============================================================="
echo ""

# Check if Python is installed
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Python found: $PYTHON_VERSION"
else
    echo "❌ Python not found! Please install Python 3.9+"
    exit 1
fi

echo ""
echo "Checking setup..."

# Run setup test
python3 test_setup.py

if [ $? -eq 0 ]; then
    echo ""
    echo "=============================================================="
    echo "  Choose Application Version"
    echo "=============================================================="
    echo ""
    echo "1. Basic App (app.py) - Simple and fast"
    echo "2. Enhanced App (app_enhanced.py) - Full features"
    echo "3. Exit"
    echo ""
    
    read -p "Enter your choice (1-3): " choice
    
    case $choice in
        1)
            echo ""
            echo "🚀 Starting Basic App..."
            echo ""
            streamlit run app.py
            ;;
        2)
            echo ""
            echo "🚀 Starting Enhanced App..."
            echo ""
            streamlit run app_enhanced.py
            ;;
        3)
            echo "Goodbye! 👋"
            exit 0
            ;;
        *)
            echo "Invalid choice. Exiting."
            exit 1
            ;;
    esac
else
    echo ""
    echo "⚠️  Setup check failed. Please fix the issues above."
    echo ""
    echo "Common fixes:"
    echo "  1. Install dependencies: pip3 install -r requirements.txt"
    echo "  2. Download model from Kaggle and place in models/best_model.h5"
    echo ""
    
    read -p "Would you like to install dependencies now? (y/n): " install
    
    if [ "$install" = "y" ] || [ "$install" = "Y" ]; then
        echo ""
        echo "Installing dependencies..."
        pip3 install -r requirements.txt
        
        echo ""
        echo "✅ Dependencies installed!"
        echo "⚠️  Don't forget to download the model file!"
        echo ""
        echo "Download from:"
        echo "  https://www.kaggle.com/datasets/gyanbardhan/vgg16"
        echo ""
    fi
fi
