# File: utils/preprocessing.py
# Helper functions for preprocessing images and EAR smoothing

import cv2
import numpy as np

def preprocess_eye_region(eye_frame):
    """
    Resize and normalize the eye region for CNN input.
    """
    resized = cv2.resize(eye_frame, (64, 64))
    normalized = resized.astype("float32") / 255.0
    return np.expand_dims(normalized, axis=0)

def smooth_ear(ear_list, window_size=5):
    """
    Apply moving average smoothing to a list of EAR values.
    """
    if len(ear_list) < window_size:
        return np.mean(ear_list)
    return np.mean(ear_list[-window_size:])
