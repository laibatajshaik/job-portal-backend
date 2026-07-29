import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.auth.email_sender import send_otp_email

def main():
    print("=== SMTP Email Connection Test ===")
    to_email = input("Enter recipient email address: ").strip()
    if not to_email:
        print("Error: Recipient email is required.")
        return
        
    print(f"\nSending test code 888888 to {to_email}...")
    success = send_otp_email(to_email, "888888")
    if success:
        print("\n[SUCCESS] SMTP connection succeeded and email was sent!")
    else:
        print("\n[FAILED] SMTP connection failed. Check your network or credentials.")

if __name__ == "__main__":
    main()
