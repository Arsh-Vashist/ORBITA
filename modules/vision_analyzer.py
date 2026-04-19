import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np
import requests
from io import BytesIO
from PIL import Image

# Load a pre-trained CNN model (MobileNetV2 is lightweight and fast)
model = MobileNetV2(weights='imagenet')

def analyze_image_bias(image_url):
    """
    Uses a CNN to detect objects in news images and 
    predicts if the image is 'Sensational' or 'Factual'.
    """
    try:
        # 1. Image Download
        response = requests.get(image_url, timeout=10)
        img = Image.open(BytesIO(response.content)).convert('RGB')
        
        # 2. Preprocessing for CNN
        img = img.resize((224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        # 3. Prediction using CNN
        preds = model.predict(img_array)
        decoded = decode_predictions(preds, top=3)[0]
        
        # 4. Logic for "Visual Bias"
        # If the model detects 'fire', 'smoke', 'protest', 'weapon', etc.
        objects = [label.lower() for (id, label, prob) in decoded]
        sensational_keywords = ['fire', 'smoke', 'weapon', 'explosion', 'fist', 'crowd']
        
        is_sensational = any(key in ' '.join(objects) for key in sensational_keywords)
        
        return {
            "detected_objects": objects,
            "visual_framing": "Sensational/Emotional" if is_sensational else "Factual/Standard",
            "confidence": float(decoded[0][2])
        }
    except Exception as e:
        return {"error": str(e)}