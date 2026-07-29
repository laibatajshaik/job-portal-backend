import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_otp_email(to_email: str, otp: str):
    
    smtp_user = os.getenv("SMTP_USER", "b3b003001@smtp-brevo.com")
    smtp_password = os.getenv("SMTP_PASSWORD", "dUQyNW8RcMIj5HpX")
    
    smtp_server = os.getenv("SMTP_SERVER", "smtp-relay.brevo.com")
    smtp_port = int(os.getenv("SMTP_PORT", "2525"))
    
    msg = MIMEMultipart()
    msg['From'] = f"Job Portal <{smtp_user}>"
    msg['To'] = to_email
    msg['Subject'] = f"Verification Code: {otp} - Job Portal Password Reset"
    
    body = f"Your verification code is: {otp}"

    msg.attach(MIMEText(body, 'plain'))
    
    try:
        if smtp_port == 465:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=5)
        else:
            server = smtplib.SMTP(smtp_server, smtp_port, timeout=5)
            server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, to_email, msg.as_string())
        server.quit()
        print(f"OTP successfully sent to real email: {to_email}")
        return True
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
        return False
