"""
Utility functions for the Plant Disease Detection application
"""

import numpy as np
from PIL import Image
import cv2


def apply_clahe(image_array):
    """
    Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) preprocessing
    as mentioned in the project documentation
    """
    # Convert to LAB color space
    lab = cv2.cvtColor(image_array, cv2.COLOR_RGB2LAB)
    
    # Split channels
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE to L channel
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    
    # Merge channels
    lab = cv2.merge([l, a, b])
    
    # Convert back to RGB
    enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
    
    return enhanced


def preprocess_with_clahe(image, target_size=(224, 224)):
    """
    Preprocess image with CLAHE enhancement
    """
    # Convert to RGB if necessary
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize image
    image = image.resize(target_size)
    
    # Convert to array
    img_array = np.array(image)
    
    # Apply CLAHE
    img_array = apply_clahe(img_array)
    
    # Normalize
    img_array = img_array.astype('float32') / 255.0
    
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array


def get_disease_info(disease_name):
    """
    Get information about the detected disease
    """
    disease_info = {
        'Apple_scab': {
            'description': 'A fungal disease causing dark, scabby lesions on leaves and fruit.',
            'treatment': 'Remove infected leaves, apply fungicides, and ensure good air circulation.'
        },
        'Black_rot': {
            'description': 'A fungal disease causing circular leaf spots and fruit rot.',
            'treatment': 'Prune infected areas, apply fungicides, and maintain orchard sanitation.'
        },
        'Cedar_apple_rust': {
            'description': 'A fungal disease causing orange spots on leaves.',
            'treatment': 'Remove nearby cedar trees, apply fungicides in spring.'
        },
        'Powdery_mildew': {
            'description': 'A fungal disease creating white powdery growth on leaves.',
            'treatment': 'Improve air circulation, apply sulfur-based fungicides.'
        },
        'Common_rust': {
            'description': 'A fungal disease causing reddish-brown pustules on leaves.',
            'treatment': 'Use resistant varieties, apply fungicides if severe.'
        },
        'Northern_Leaf_Blight': {
            'description': 'A fungal disease causing long, elliptical lesions on leaves.',
            'treatment': 'Rotate crops, use resistant hybrids, apply fungicides.'
        },
        'Cercospora_leaf_spot': {
            'description': 'A fungal disease causing gray leaf spots.',
            'treatment': 'Crop rotation, fungicide application, remove infected debris.'
        },
        'Bacterial_spot': {
            'description': 'A bacterial disease causing dark spots on leaves and fruit.',
            'treatment': 'Use disease-free seeds, apply copper-based bactericides.'
        },
        'Early_blight': {
            'description': 'A fungal disease causing dark spots with concentric rings.',
            'treatment': 'Remove infected leaves, apply fungicides, practice crop rotation.'
        },
        'Late_blight': {
            'description': 'A serious disease causing water-soaked lesions and plant death.',
            'treatment': 'Apply fungicides preventatively, destroy infected plants immediately.'
        },
        'Leaf_Mold': {
            'description': 'A fungal disease causing yellow spots on upper leaf surfaces.',
            'treatment': 'Improve ventilation, reduce humidity, apply fungicides.'
        },
        'Septoria_leaf_spot': {
            'description': 'A fungal disease causing circular spots with gray centers.',
            'treatment': 'Remove infected leaves, apply fungicides, mulch around plants.'
        },
        'Target_Spot': {
            'description': 'A fungal disease causing concentric ring patterns on leaves.',
            'treatment': 'Practice crop rotation, apply fungicides, maintain plant spacing.'
        },
        'Tomato_Yellow_Leaf_Curl_Virus': {
            'description': 'A viral disease causing yellowing and curling of leaves.',
            'treatment': 'Control whitefly vectors, remove infected plants, use resistant varieties.'
        },
        'Tomato_mosaic_virus': {
            'description': 'A viral disease causing mottled leaves and reduced fruit quality.',
            'treatment': 'Use virus-free seeds, sanitize tools, remove infected plants.'
        },
        'healthy': {
            'description': 'No disease detected. The plant appears healthy!',
            'treatment': 'Continue regular maintenance and monitoring.'
        }
    }
    
    # Try to find matching disease info
    for key, info in disease_info.items():
        if key.lower() in disease_name.lower():
            return info
    
    return {
        'description': 'Disease information not available.',
        'treatment': 'Consult with a local agricultural extension service.'
    }
