# File: utils/file_io.py
# Handles logging of blink data and fatigue scores to CSV

import csv
from datetime import datetime
import os

RESULTS_PATH = "results"

# Ensure results directory exists
os.makedirs(RESULTS_PATH, exist_ok=True)

BLINK_LOG = os.path.join(RESULTS_PATH, "blink_log.csv")
FATIGUE_LOG = os.path.join(RESULTS_PATH, "fatigue_log.csv")
ALERT_LOG = os.path.join(RESULTS_PATH, "alert_log.csv")
SUMMARY_PDF = os.path.join(RESULTS_PATH, "summary_report.pdf")


def log_blink(ear, blink_detected):
    with open(BLINK_LOG, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), f"{ear:.4f}", int(blink_detected)])

def log_fatigue_score(score):
    with open(FATIGUE_LOG, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), f"{score:.4f}"])

# ✅ Supports detailed reason like YAWN_DETECTED or ALERT_TRIGGERED
def log_alert(score, reason="ALERT_TRIGGERED"):
    with open(ALERT_LOG, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), f"{score:.4f}", reason])