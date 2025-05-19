import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_report_email(to_email, full_name, selected_date, result_summary, wound_size):
    from_email = "noreply@example.com"  # Replace with your 'noreply' address
    subject = "Diabetic Wound Analysis Report"
    
    body = f"""Dear {full_name},

Your wound analysis report for {selected_date} is ready.

Result: {result_summary}
Estimated wound size: {wound_size} cm²

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
        # Use a real SMTP server (example: Gmail SMTP settings)
        smtp = smtplib.SMTP("smtp.gmail.com", 587)
        smtp.starttls()
        smtp.login("your_gmail@gmail.com", "your_app_password")
        smtp.send_message(msg)
        smtp.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
