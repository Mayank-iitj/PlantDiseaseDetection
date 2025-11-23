"""
Test script for the Plant Disease Detection application
Run this to verify the setup and model loading
"""

import os
import sys
from pathlib import Path

def test_imports():
    """Test if all required packages are installed"""
    print("Testing imports...")
    
    required_packages = {
        'streamlit': 'streamlit',
        'tensorflow': 'tensorflow',
        'PIL': 'pillow',
        'numpy': 'numpy',
    }
    
    optional_packages = {
        'cv2': 'opencv-python',
        'gdown': 'gdown'
    }
    
    all_good = True
    
    for module, package in required_packages.items():
        try:
            __import__(module)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} NOT installed - REQUIRED")
            all_good = False
    
    for module, package in optional_packages.items():
        try:
            __import__(module)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"⚠️  {package} NOT installed - Optional")
    
    return all_good

def test_model_file():
    """Check if model file exists"""
    print("\nTesting model file...")
    
    model_path = Path("models/best_model.h5")
    
    if model_path.exists():
        size_mb = model_path.stat().st_size / (1024 * 1024)
        print(f"✅ Model file found: {model_path}")
        print(f"   Size: {size_mb:.2f} MB")
        return True
    else:
        print(f"❌ Model file NOT found at: {model_path}")
        print("   Please download and place your model file in the 'models' directory")
        return False

def test_directory_structure():
    """Check if required directories exist"""
    print("\nTesting directory structure...")
    
    required_dirs = ['models', '.streamlit']
    all_good = True
    
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"✅ Directory exists: {dir_name}/")
        else:
            print(f"❌ Directory missing: {dir_name}/")
            all_good = False
    
    return all_good

def test_streamlit_config():
    """Check if Streamlit config exists"""
    print("\nTesting Streamlit configuration...")
    
    config_path = Path(".streamlit/config.toml")
    
    if config_path.exists():
        print(f"✅ Streamlit config found: {config_path}")
        return True
    else:
        print(f"⚠️  Streamlit config not found at: {config_path}")
        print("   The app will use default settings")
        return False

def test_app_file():
    """Check if app.py exists"""
    print("\nTesting application file...")
    
    app_path = Path("app.py")
    
    if app_path.exists():
        print(f"✅ Application file found: {app_path}")
        return True
    else:
        print(f"❌ Application file NOT found: {app_path}")
        return False

def main():
    print("=" * 50)
    print("Plant Disease Detection - Setup Test")
    print("=" * 50)
    
    results = {
        'imports': test_imports(),
        'model': test_model_file(),
        'directories': test_directory_structure(),
        'config': test_streamlit_config(),
        'app': test_app_file()
    }
    
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    critical_tests = ['imports', 'model', 'app']
    critical_passed = all(results[test] for test in critical_tests)
    
    if critical_passed:
        print("✅ All critical tests passed!")
        print("\nYou can now run the application with:")
        print("   streamlit run app.py")
    else:
        print("❌ Some critical tests failed!")
        print("\nPlease fix the issues above before running the application.")
        
        if not results['imports']:
            print("\nTo install required packages:")
            print("   pip install -r requirements.txt")
        
        if not results['model']:
            print("\nTo download a model:")
            print("   1. Visit: https://www.kaggle.com/datasets/gyanbardhan/vgg16")
            print("   2. Download the model file")
            print("   3. Place it in: models/best_model.h5")
    
    print("\n" + "=" * 50)
    
    return critical_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
