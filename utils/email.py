import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import streamlit as st  # required to access secrets

def send_report_email(to_email, full_name, selected_date, result_summary, wound_size):
    from_email = st.secrets["email"]["address"]
    password = st.secrets["email"]["app_password"]
    subject = "Diabetic Wound Analysis Report"
    
    body = f"""Dear {full_name},

Your wound analysis report for {selected_date} is ready.

Result: 
{result_summary}

Total estimated wound size: {wound_size:.2f} cm²

This email was sent automatically. Please do not reply.

Best regards,
Your AI Wound Monitoring Assistant
"""

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        smtp = smtplib.SMTP("smtp.gmail.com", 587)
        smtp.starttls()
        smtp.login(from_email, password)
        smtp.send_message(msg)
        smtp.quit()
        return True
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
        return False
