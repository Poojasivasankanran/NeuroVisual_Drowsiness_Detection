# File: dashboard/plots.py
# Helper functions to generate plots for Streamlit dashboard

import matplotlib.pyplot as plt

def plot_ear_trend(df):
    fig, ax = plt.subplots()
    ax.plot(df["timestamp"], df["EAR"], label="EAR")
    ax.set_xlabel("Time")
    ax.set_ylabel("EAR")
    ax.set_title("Eye Aspect Ratio Over Time")
    ax.legend()
    fig.autofmt_xdate()
    return fig

def plot_fatigue_score(df):
    fig, ax = plt.subplots()
    ax.plot(df["timestamp"], df["Score"], color="orange", label="Fatigue Score")
    ax.set_xlabel("Time")
    ax.set_ylabel("Fatigue Score")
    ax.set_title("Fatigue Score Trend")
    ax.legend()
    fig.autofmt_xdate()
    return fig
