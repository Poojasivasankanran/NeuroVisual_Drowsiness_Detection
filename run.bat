@echo off
echo 🚗 NeuroVisual Drowsiness System Launcher

echo 🧠 Running main.py...
python main.py

echo 📄 Generating PDF report...
python utils\pdf_report_generator.py

echo 🌐 Launching Streamlit dashboard...
streamlit run dashboard\app.py
