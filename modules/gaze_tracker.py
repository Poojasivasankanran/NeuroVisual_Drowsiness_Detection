# File: modules/gaze_tracker.py

import numpy as np
from scipy.spatial import distance as dist
import cv2
import dlib

# EAR = Eye Aspect Ratio formula
def get_ear(gray, face, predictor):
    shape = predictor(gray, face)
    coords = np.array([(shape.part(i).x, shape.part(i).y) for i in range(68)])

    left_eye = coords[36:42]
    right_eye = coords[42:48]

    left_ear = calculate_ear(left_eye)
    right_ear = calculate_ear(right_eye)

    return (left_ear + right_ear) / 2.0

def calculate_ear(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear
