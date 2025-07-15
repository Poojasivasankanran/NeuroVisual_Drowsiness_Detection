# File: modules/fatigue_predictor.py

import cv2
import numpy as np
import tensorflow as tf
import joblib
from utils.file_io import log_fatigue_score

cnn_model = tf.keras.models.load_model("models/cnn_eye_classifier.h5")
meta_model = joblib.load("models/meta_classifier.pkl")

def preprocess_eye_region(frame):
    resized = cv2.resize(frame, (200, 200))  # matches CNN input
    norm = resized.astype("float32") / 255.0
    return norm

def predict_fatigue(frame, ear):
    # Prepare CNN input
    eye_img = preprocess_eye_region(frame)
    eye_img = np.expand_dims(eye_img, axis=0)

    # CNN prediction: [open_prob, closed_prob, yawn_prob]
    cnn_output = cnn_model.predict(eye_img, verbose=0)[0]
    # Fallback handling if only 2 classes are returned (open/closed)
    cnn_open = cnn_output[0] if len(cnn_output) > 0 else 0.5
    cnn_closed = cnn_output[1] if len(cnn_output) > 1 else 0.5
    cnn_yawn = cnn_output[2] if len(cnn_output) > 2 else 0.0

    

    # Calculate EAR-related score
    ear_score = 1.0 - min(ear / 0.3, 1.0)

    # Prepare combined feature vector
    combined = np.array([[ear, cnn_open, cnn_closed, cnn_yawn, ear_score, np.mean(cnn_output)]])

    # Meta model prediction (RandomForest)
    fatigue_score = meta_model.predict_proba(combined)[0][1]

    # Log result
    log_fatigue_score(fatigue_score)

    # ✅ Return both values to prevent unpacking error
    return fatigue_score, cnn_output
