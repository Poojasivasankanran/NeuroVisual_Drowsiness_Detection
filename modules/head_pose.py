# File: modules/head_pose.py
# Estimate head pose using solvePnP and facial landmarks

import numpy as np
import cv2

def estimate_head_pose(landmarks):
    model_points = np.array([
        (0.0, 0.0, 0.0),           # Nose tip
        (0.0, -330.0, -65.0),      # Chin
        (-225.0, 170.0, -135.0),   # Left eye corner
        (225.0, 170.0, -135.0),    # Right eye corner
        (-150.0, -150.0, -125.0),  # Left mouth corner
        (150.0, -150.0, -125.0)    # Right mouth corner
    ])

    image_points = np.array(landmarks, dtype='double')  # Must be 6 points in order

    # Camera parameters (assumed for standard webcam)
    focal_length = 640
    center = (320, 240)
    camera_matrix = np.array(
        [[focal_length, 0, center[0]],
         [0, focal_length, center[1]],
         [0, 0, 1]], dtype='double'
    )
    dist_coeffs = np.zeros((4, 1))  # No lens distortion

    # Solve PnP to estimate rotation and translation
    success, rotation_vector, translation_vector = cv2.solvePnP(
        model_points, image_points, camera_matrix, dist_coeffs
    )

    return rotation_vector, translation_vector
