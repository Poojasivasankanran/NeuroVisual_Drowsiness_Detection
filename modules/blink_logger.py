# File: modules/blink_logger.py
# Calculates EAR and detects blink events

from scipy.spatial import distance as dist
from utils.file_io import log_blink

def calculate_ear(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def detect_blink(left_eye, right_eye, threshold):
    left_ear = calculate_ear(left_eye)
    right_ear = calculate_ear(right_eye)
    ear = (left_ear + right_ear) / 2.0

    blink_detected = ear < threshold

    # ✅ Log blink event to CSV
    log_blink(ear, blink_detected)

    return ear, blink_detected
