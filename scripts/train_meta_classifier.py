# File: scripts/train_meta_classifier.py
# Trains a Random Forest meta-classifier from CNN and LSTM outputs

import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

def generate_dummy_features(num_samples=500):
    """
    Simulates CNN + LSTM features.
    CNN: [eye_prob_open, eye_prob_closed, yawn_prob]
    LSTM: [blink_rate, blink_duration, interval_var]
    """
    cnn_features = np.random.rand(num_samples, 3)
    lstm_features = np.random.rand(num_samples, 3)
    fused_features = np.hstack((cnn_features, lstm_features))

    labels = np.random.randint(0, 2, num_samples)  # 0: awake, 1: drowsy
    return fused_features, labels

def train_meta_classifier():
    X, y = generate_dummy_features()

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/meta_classifier.pkl")
    print("✅ Meta-classifier saved to models/meta_classifier.pkl")

if __name__ == "__main__":
    train_meta_classifier()
