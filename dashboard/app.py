# File: dashboard/app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from io import BytesIO
from stats import get_total_blinks, get_alert_count, get_latest_fatigue_score

st.set_page_config(page_title="NeuroVisual Drowsiness Dashboard", layout="wide", page_icon="🚗")
st.title("🚗 NeuroVisual Drowsiness Detection - Monitoring Dashboard")

RESULTS_DIR = "results"

# Load logs
def load_csv(filepath, cols):
    if os.path.exists(filepath):
        return pd.read_csv(filepath, header=None, names=cols)
    else:
        return pd.DataFrame(columns=cols)

blink_df = load_csv(os.path.join(RESULTS_DIR, "blink_log.csv"), ["timestamp", "EAR", "Blink"])
fatigue_df = load_csv(os.path.join(RESULTS_DIR, "fatigue_log.csv"), ["timestamp", "Score"])
alert_df = load_csv(os.path.join(RESULTS_DIR, "alert_log.csv"), ["timestamp", "Score", "Status"])

# Main Metrics
st.metric("Total Blinks", get_total_blinks())
st.metric("Latest Fatigue Score", f"{get_latest_fatigue_score():.2f}")
st.metric("Alerts Triggered", get_alert_count())
yawn_count = len(alert_df[alert_df["Status"] == "YAWN_DETECTED"]) if not alert_df.empty else 0
st.metric("Yawns Detected", yawn_count)

# 📊 Tabbed Layout
tab1, tab2, tab3 = st.tabs(["👁️ EAR Trend", "📉 Fatigue Score", "😮 Yawn Frequency"])

with tab1:
    st.subheader("👁️ EAR Over Time")
    if not blink_df.empty:
        st.line_chart(blink_df.set_index("timestamp")[["EAR"]])
    else:
        st.info("No blink data yet.")

with tab2:
    st.subheader("📉 Fatigue Score Trend")
    if not fatigue_df.empty:
        st.line_chart(fatigue_df.set_index("timestamp")[["Score"]])
    else:
        st.info("No fatigue score logged.")

with tab3:
    st.subheader("😮 Yawn Frequency per Minute")
    if not alert_df.empty:
        yawn_df = alert_df[alert_df["Status"] == "YAWN_DETECTED"].copy()
        yawn_df["timestamp"] = pd.to_datetime(yawn_df["timestamp"])
        yawn_df["minute"] = yawn_df["timestamp"].dt.strftime("%H:%M")
        yawns_per_minute = yawn_df.groupby("minute").size().reset_index(name="Yawn Count")

        if not yawns_per_minute.empty:
            st.bar_chart(data=yawns_per_minute.set_index("minute"))
        else:
            st.info("No yawn data available.")
    else:
        st.info("No yawn data available.")

# 🚨 Alert Log Section
st.divider()
st.subheader("🚨 Recent Alert History")
if not alert_df.empty:
    st.dataframe(alert_df.tail(10), use_container_width=True)
else:
    st.info("No alerts yet.")

# 📤 Export Section
st.divider()
st.subheader("📤 Export Logs")

def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

if not alert_df.empty:
    st.download_button("⬇️ Download Alert Log (CSV)", data=convert_df_to_csv(alert_df), file_name="alert_log.csv", mime='text/csv')

if not fatigue_df.empty:
    st.download_button("⬇️ Download Fatigue Log (CSV)", data=convert_df_to_csv(fatigue_df), file_name="fatigue_log.csv", mime='text/csv')

# Optional: Export as PDF (using BytesIO and matplotlib — coming next if needed)
# PDF Report Download
st.divider()
st.subheader("📄 Download Full Summary Report (PDF)")

pdf_path = "results/summary_report.pdf"
if os.path.exists(pdf_path):
    with open(pdf_path, "rb") as f:
        st.download_button(
            label="⬇️ Download Report",
            data=f,
            file_name="summary_report.pdf",
            mime="application/pdf"
        )
else:
    st.warning("PDF report not found. Please run the PDF generator first.")
