# File: utils/email_sender.py
import smtplib
import os
from email.message import EmailMessage

def send_report_via_email(to_email, subject, body="Please find the attached NeuroVisual report.", attachment_path="results/summary_report.pdf"):
    from_email = "your_email@gmail.com"  # 🔁 Replace
    app_password = "your_app_password"   # 🔁 Use app password, not regular password

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg.set_content(body)

    if os.path.exists(attachment_path):
        with open(attachment_path, "rb") as f:
            file_data = f.read()
            msg.add_attachment(file_data, maintype="application", subtype="pdf", filename="summary_report.pdf")
    else:
        print("⚠️ PDF not found.")
        return

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(from_email, app_password)
            smtp.send_message(msg)
            print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
