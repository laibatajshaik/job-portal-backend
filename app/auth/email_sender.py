import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import json
import urllib.request

def send_otp_email(to_email: str, otp: str):
    brevo_key = os.getenv("BREVO_API_KEY")
    
    if brevo_key:
        try:
            url = 'https://api.brevo.com/v3/smtp/email'
            headers = {
                'accept': 'application/json',
                'api-key': brevo_key,
                'content-type': 'application/json'
            }
            payload = {
                'sender': {'name': 'Job Portal', 'email': 'laibataj1301@gmail.com'},
                'to': [{'email': to_email}],
                'subject': f"Verification Code: {otp} - Job Portal Password Reset",
                'textContent': f"Your verification code is: {otp}"
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode('utf-8'),
                headers=headers,
                method='POST'
            )
            with urllib.request.urlopen(req) as res:
                print(f"OTP successfully sent via Brevo HTTP API to {to_email}")
                return True
        except Exception as e:
            print(f"Failed to send email via Brevo API to {to_email}: {e}")
            pass

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
        print(f"OTP successfully sent via SMTP to {to_email}")
        return True
    except Exception as e:
        print(f"Failed to send email via SMTP to {to_email}: {e}")
        return False

def send_notification_email(to_email: str, subject: str, body: str):
    brevo_key = os.getenv("BREVO_API_KEY")
    if brevo_key:
        try:
            url = 'https://api.brevo.com/v3/smtp/email'
            headers = {
                'accept': 'application/json',
                'api-key': brevo_key,
                'content-type': 'application/json'
            }
            payload = {
                'sender': {'name': 'Job Portal', 'email': 'laibataj1301@gmail.com'},
                'to': [{'email': to_email}],
                'subject': subject,
                'textContent': body
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode('utf-8'),
                headers=headers,
                method='POST'
            )
            with urllib.request.urlopen(req) as res:
                print(f"Notification email successfully sent via Brevo HTTP API to {to_email}")
                return True
        except Exception as e:
            print(f"Failed to send notification via Brevo API to {to_email}: {e}")
            pass

    smtp_user = os.getenv("SMTP_USER", "b3b003001@smtp-brevo.com")
    smtp_password = os.getenv("SMTP_PASSWORD", "dUQyNW8RcMIj5HpX")
    smtp_server = os.getenv("SMTP_SERVER", "smtp-relay.brevo.com")
    smtp_port = int(os.getenv("SMTP_PORT", "2525"))
    
    msg = MIMEMultipart()
    msg['From'] = f"Job Portal <{smtp_user}>"
    msg['To'] = to_email
    msg['Subject'] = subject
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
        print(f"Notification email successfully sent via SMTP to {to_email}")
        return True
    except Exception as e:
        print(f"Failed to send notification via SMTP to {to_email}: {e}")
        return False
