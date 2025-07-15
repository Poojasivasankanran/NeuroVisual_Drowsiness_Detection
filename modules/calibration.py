import cv2
from modules.gaze_tracker import get_ear


def calibrate_threshold(detector, predictor):
    print("🔧 Calibration started... Please look at the camera and blink naturally.")
    ear_values = []
    cap = cv2.VideoCapture(0)
    for _ in range(100):
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        for face in faces:
            ear = get_ear(gray, face, predictor)
            if ear:
                ear_values.append(ear)
    cap.release()
    threshold = sum(ear_values) / len(ear_values) if ear_values else 0.25
    print(f"✅ Calibration complete. EAR_THRESHOLD = {threshold:.3f}")
    return threshold
