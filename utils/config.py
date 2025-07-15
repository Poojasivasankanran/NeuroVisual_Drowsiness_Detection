# File: utils/config.py
import json

CONFIG_PATH = "config.json"

def load_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️ config.json not found! Using fallback values.")
        return {
            "EAR_THRESHOLD": 0.22,
            "YAWN_PROB_THRESHOLD": 0.6,
            "ALERT_HOLD_FRAMES": 5,
            "ALERT_COOLDOWN_TIME": 10
        }
