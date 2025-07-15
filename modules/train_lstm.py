# File: modules/train_lstm.py
# Script to train an LSTM model on blink feature sequences

import numpy as np
import tensorflow as tf
import os

def load_training_data():
    """
    Simulate some dummy data.
    Replace this with real blink/EAR sequences later.
    """
    X = np.random.rand(100, 10, 3)  # 100 sequences, 10 timesteps, 3 features
    y = np.random.randint(0, 2, 100)  # Binary labels: 0 = awake, 1 = drowsy
    return X, y

def train_lstm_model():
    X, y = load_training_data()

    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.LSTM(64, input_shape=(X.shape[1], X.shape[2]), return_sequences=False))
    model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Make sure models directory exists
    os.makedirs("models", exist_ok=True)

    checkpoint = tf.keras.callbacks.ModelCheckpoint(
        "models/lstm_fatigue_predictor.h5",
        save_best_only=True,
        monitor='val_loss'
    )

    model.fit(X, y, epochs=20, batch_size=8, validation_split=0.2, callbacks=[checkpoint])

    print("✅ LSTM model trained and saved to models/lstm_fatigue_predictor.h5")

if __name__ == "__main__":
    train_lstm_model()
