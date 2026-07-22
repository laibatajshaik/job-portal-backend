import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_otp_email(to_email: str, otp: str):
    # Live Gmail noreply setup for Job Portal demo/staging emails
    smtp_user = os.getenv("SMTP_USER", "jobportal.noreply.otp@gmail.com")
    smtp_password = os.getenv("SMTP_PASSWORD", "vxtg nggj isqk kofj")
    
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    
    msg = MIMEMultipart()
    msg['From'] = f"Job Portal <{smtp_user}>"
    msg['To'] = to_email
    msg['Subject'] = f"Verification Code: {otp} - Job Portal Password Reset"
    
    body = f"""Hello,

We received a request to reset the password for your Job Portal account associated with {to_email}.

Your 6-digit verification code (OTP) is:

👉  {otp}  👈

Please enter this verification code in the Reset Password form to update your account password. This code will expire in 10 minutes.

If you did not request a password reset, you can safely ignore this email.

Best regards,
The Job Portal Team
"""
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, to_email, msg.as_string())
        server.quit()
        print(f"OTP successfully sent to real email: {to_email}")
        return True
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
        return False
