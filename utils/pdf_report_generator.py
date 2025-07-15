# File: utils/pdf_report_generator.py

import os
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime

RESULTS_PATH = "results"
OUTPUT_PATH = os.path.join(RESULTS_PATH, "summary_report.pdf")

def generate_report():
    # Load data
    blink_df = pd.read_csv(os.path.join(RESULTS_PATH, "blink_log.csv"), header=None, names=["timestamp", "EAR", "Blink"])
    fatigue_df = pd.read_csv(os.path.join(RESULTS_PATH, "fatigue_log.csv"), header=None, names=["timestamp", "Score"])
    alert_df = pd.read_csv(os.path.join(RESULTS_PATH, "alert_log.csv"), header=None, names=["timestamp", "Score", "Status"])

    # Start PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "🧠 NeuroVisual Drowsiness Detection Report", ln=True)

    # Summary stats
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.cell(0, 10, f"Total Blinks: {int(blink_df['Blink'].sum())}", ln=True)
    pdf.cell(0, 10, f"Total Alerts: {len(alert_df)}", ln=True)
    pdf.cell(0, 10, f"Yawns Detected: {len(alert_df[alert_df['Status'] == 'YAWN_DETECTED'])}", ln=True)
    pdf.cell(0, 10, f"Average Fatigue Score: {fatigue_df['Score'].astype(float).mean():.2f}", ln=True)
    
    # Charts
    chart_path = os.path.join(RESULTS_PATH, "chart_temp.png")

    # EAR Chart
    plt.figure(figsize=(6,3))
    plt.plot(blink_df["EAR"].astype(float), color="green")
    plt.title("EAR (Eye Aspect Ratio) Over Time")
    plt.xlabel("Frame")
    plt.ylabel("EAR")
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()
    pdf.image(chart_path, w=180)

    # Fatigue Score Chart
    plt.figure(figsize=(6,3))
    plt.plot(fatigue_df["Score"].astype(float), color="red")
    plt.title("Fatigue Score Over Time")
    plt.xlabel("Frame")
    plt.ylabel("Score")
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()
    pdf.image(chart_path, w=180)

    # Yawn Bar Chart
    yawn_df = alert_df[alert_df["Status"] == "YAWN_DETECTED"].copy()
    if not yawn_df.empty:
        yawn_df["timestamp"] = pd.to_datetime(yawn_df["timestamp"])
        yawn_df["minute"] = yawn_df["timestamp"].dt.strftime("%H:%M")
        yawn_counts = yawn_df.groupby("minute").size()
        yawn_counts.plot(kind="bar", figsize=(6,3), color="blue", title="Yawn Count per Minute")
        plt.xlabel("Time")
        plt.ylabel("Yawn Count")
        plt.tight_layout()
        plt.savefig(chart_path)
        plt.close()
        pdf.image(chart_path, w=180)

    # Save PDF
    pdf.output(OUTPUT_PATH)
    print(f"✅ Report saved to {OUTPUT_PATH}")
