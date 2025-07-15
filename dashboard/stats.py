# File: dashboard/stats.py
# Tracks and displays system statistics like blink count, alert count, and fatigue

import pandas as pd
import os

RESULTS_DIR = "results"

def get_total_blinks():
    file_path = os.path.join(RESULTS_DIR, "blink_log.csv")
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path, header=None, names=["timestamp", "EAR", "Blink"])
            return int(df["Blink"].sum())
        except Exception as e:
            print(f"❌ Blink log error: {e}")
    return 0

def get_alert_count():
    file_path = os.path.join(RESULTS_DIR, "alert_log.csv")
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path, header=None, names=["timestamp", "Score", "Status"])
            return len(df)
        except Exception as e:
            print(f"❌ Alert log error: {e}")
    return 0

def get_latest_fatigue_score():
    file_path = os.path.join(RESULTS_DIR, "fatigue_log.csv")
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path, header=None, names=["timestamp", "Score"])
            if not df.empty:
                return float(df["Score"].iloc[-1])
        except Exception as e:
            print(f"❌ Fatigue log error: {e}")
    return 0.0
