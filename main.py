# File: main.py

import cv2
import dlib
import pygame
import time
from imutils import face_utils

from modules.calibration import calibrate_threshold
from modules.gaze_tracker import get_ear
from modules.blink_logger import detect_blink
from modules.fatigue_predictor import predict_fatigue
from modules.alerts import play_sound_alert, send_telegram_alert
from utils.file_io import log_alert
from utils.config import load_config

# 🔊 Init alarm system
pygame.mixer.init()

# 🧠 Load thresholds from config file
config = load_config()
EAR_THRESHOLD = config["EAR_THRESHOLD"]
YAWN_PROB_THRESHOLD = config["YAWN_PROB_THRESHOLD"]
ALERT_HOLD_FRAMES = config["ALERT_HOLD_FRAMES"]
ALERT_COOLDOWN_TIME = config["ALERT_COOLDOWN_TIME"]

# 🔍 Load face detector and shape predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor/shape_predictor_68_face_landmarks.dat")

# 🔧 Calibrate EAR (can be skipped if config used directly)
EAR_THRESHOLD = calibrate_threshold(detector, predictor)

# 🎥 Start webcam
cap = cv2.VideoCapture(0)
print("📷 Starting real-time drowsiness detection... Press 'q' to quit.")

# 🚨 Initialize alert counters
alert_counter = 0
last_alert_time = 0

# ✅ Check alerts_enabled.txt flag
def alerts_enabled():
    try:
        with open("alerts_enabled.txt", "r") as f:
            return f.read().strip().lower() == "true"
    except:
        return True  # default ON

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        shape = predictor(gray, face)
        shape_np = face_utils.shape_to_np(shape)

        # 🔵 Draw 68 landmark points
        for (x, y) in shape_np:
            cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

        leftEye = shape_np[36:42]
        rightEye = shape_np[42:48]

        # 👁️ EAR and blink detection
        ear, blink_detected = detect_blink(leftEye, rightEye, EAR_THRESHOLD)

        # 🧠 Fatigue prediction (CNN + Meta)
        fatigue_score, cnn_output = predict_fatigue(frame, ear)

        # 😮 Yawn logic
        ear_drowsy = ear < EAR_THRESHOLD
        yawn_detected = cnn_output[2] > YAWN_PROB_THRESHOLD
        current_time = time.time()

        # 🚨 Trigger alert if needed
        if (ear_drowsy or yawn_detected) and alerts_enabled():
            alert_counter += 1
            if alert_counter >= ALERT_HOLD_FRAMES and (current_time - last_alert_time) > ALERT_COOLDOWN_TIME:
                print("😴 Drowsiness condition met. Triggering alerts.")
                play_sound_alert()
                send_telegram_alert(f"Fatigue Score: {fatigue_score:.2f} | EAR: {ear:.2f}")
                log_alert(fatigue_score, reason="EAR_YAWN_ALERT")
                last_alert_time = current_time
                alert_counter = 0
        else:
            alert_counter = 0

        # 🖼️ Overlay status
        cv2.putText(frame, f"EAR: {ear:.2f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(frame, f"Fatigue: {fatigue_score:.2f}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        if yawn_detected:
            cv2.putText(frame, "YAWN 😮", (10, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 100, 255), 2)

    # 🎥 Display the video frame
    cv2.imshow("NeuroVisual Drowsiness Detector", frame)

    # ⌨️ Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
