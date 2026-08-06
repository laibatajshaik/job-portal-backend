from fastapi import APIRouter, HTTPException
from app.schemas.user import UserRegister
from app.auth.jwt_handler import create_access_token
from app.db import load_users, save_users
from app.auth.email_sender import send_otp_email

import random
import os
import smtplib
import urllib.request
import urllib.error
import json
import base64

from email.mime.text import MIMEText


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

active_otps = {}

@router.post("/register")
def register(user: UserRegister):

    db_users = load_users()

    for u in db_users:

        if u["email"].lower() == user.email.lower():

            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

    new_user = {
        "name": user.name,
        "email": user.email,
        "password": user.password,
        "role": user.role
    }

    db_users.append(new_user)

    save_users(db_users)

    token = create_access_token({
        "sub": user.email
    })

    return {
        "message": "User Registered Successfully",
        "access_token": token,
        "token_type": "bearer"
    }

@router.post("/login")
def login(user: UserRegister):

    db_users = load_users()

    found_user = None

    for u in db_users:

        if (
            u["email"].lower() == user.email.lower()
            and u["password"] == user.password
        ):

            found_user = u
            break

    if not found_user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token({
        "sub": found_user["email"]
    })

    return {
        "message": "Login Successful",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "name": found_user["name"],
            "email": found_user["email"],
            "role": found_user["role"]
        }
    }

@router.get("/test-email-status")
def test_email_status(to: str):

    res = {}
    
    resend_key = os.getenv("RESEND_API_KEY")

    res["resend_key_configured"] = bool(resend_key)

    if resend_key:

        try:

            url = "https://api.resend.com/emails"

            headers = {
                "Authorization": f"Bearer {resend_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "from": "onboarding@resend.dev",
                "to": to,
                "subject": "Test Resend",
                "html": "<p>Test</p>"
            }

            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST"
            )

            with urllib.request.urlopen(req) as r:

                res["resend_success"] = True

                res["resend_response"] = (
                    r.read().decode("utf-8")
                )

        except Exception as e:

            err_body = (
                e.read().decode("utf-8")
                if hasattr(e, "read")
                else ""
            )

            res["resend_success"] = False
            res["resend_error"] = str(e)
            res["resend_error_body"] = err_body

    brevo_key = os.getenv("BREVO_API_KEY")

    res["brevo_key_configured"] = bool(brevo_key)

    if brevo_key:

        try:

            url = "https://api.brevo.com/v3/smtp/email"

            headers = {
                "accept": "application/json",
                "api-key": brevo_key,
                "content-type": "application/json"
            }

            payload = {
                "sender": {
                    "name": "Job Portal",
                    "email": "laibataj1301@gmail.com"
                },
                "to": [
                    {
                        "email": to
                    }
                ],
                "subject": "Test Brevo API",
                "textContent": "Test"
            }

            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST"
            )

            with urllib.request.urlopen(req) as r:

                res["brevo_success"] = True

                res["brevo_response"] = (
                    r.read().decode("utf-8")
                )

        except Exception as e:

            err_body = (
                e.read().decode("utf-8")
                if hasattr(e, "read")
                else ""
            )

            res["brevo_success"] = False
            res["brevo_error"] = str(e)
            res["brevo_error_body"] = err_body

    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER")

    smtp_port = int(
        os.getenv("SMTP_PORT", "2525")
    )

    if smtp_user and smtp_password and smtp_server:

        try:

            msg = MIMEText("Test SMTP")

            msg["Subject"] = "Test SMTP"
            msg["From"] = smtp_user
            msg["To"] = to

            server = smtplib.SMTP(
                smtp_server,
                smtp_port,
                timeout=5
            )

            server.starttls()

            server.login(
                smtp_user,
                smtp_password
            )

            server.sendmail(
                smtp_user,
                [to],
                msg.as_string()
            )

            server.quit()

            res["smtp_success"] = True

        except Exception as e:

            res["smtp_success"] = False
            res["smtp_error"] = str(e)

    else:

        res["smtp_success"] = False

        res["smtp_error"] = (
            "SMTP credentials not fully configured "
            "in environment"
        )

    return res

@router.post("/forgot-password")
def forgot_password(payload: dict):

    email = payload.get("email")

    if not email:

        raise HTTPException(
            status_code=400,
            detail="Email is required"
        )

    email = email.strip().lower()

    otp = str(
        random.randint(100000, 999999)
    )

    active_otps[email] = otp

    print(
        f"\n>>> [OTP GENERATED] "
        f"Email: {email} | Code: {otp}\n"
    )

    email_sent = send_otp_email(
        email,
        otp
    )

    return {
        "message": (
            "Verification code sent to registered email address"
            if email_sent
            else "Generated verification code internally"
        ),
        "email": email
    }

@router.post("/reset-password")
def reset_password(payload: dict):

    email = payload.get("email")
    code = payload.get("code")
    new_password = payload.get("new_password")

    if not email or not code or not new_password:

        raise HTTPException(
            status_code=400,
            detail=(
                "Email, verification code, and "
                "new password are required"
            )
        )

    email = email.strip().lower()

    expected_code = active_otps.get(email)

    if (
        not expected_code
        or expected_code != str(code).strip()
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid or expired verification code"
        )

    db_users = load_users()

    user_updated = False

    for u in db_users:

        if u["email"].lower() == email:

            u["password"] = new_password

            user_updated = True

            break

    if user_updated:

        save_users(db_users)

    active_otps.pop(
        email,
        None
    )

    return {
        "message": "Password reset successfully",
        "email": email
    }

@router.post("/google-login")
def google_login(payload: dict):

    token = payload.get("token")

    if not token:

        raise HTTPException(
            status_code=400,
            detail="Google authentication token is required"
        )

    data = None

    try:

        url = (
            "https://oauth2.googleapis.com/"
            f"tokeninfo?id_token={token}"
        )

        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            }
        )

        with urllib.request.urlopen(req) as response:

            data = json.loads(
                response.read().decode("utf-8")
            )

    except Exception as online_err:

        print(
            "Google online verification failed:",
            online_err
        )

        try:

            parts = token.split(".")

            if len(parts) == 3:

                payload_b64 = parts[1]

                padded = (
                    payload_b64
                    + "=" * (
                        (4 - len(payload_b64) % 4) % 4
                    )
                )

                decoded_bytes = (
                    base64.urlsafe_b64decode(
                        padded
                    )
                )

                data = json.loads(
                    decoded_bytes.decode("utf-8")
                )

        except Exception as local_err:

            print(
                "Local JWT decoding failed:",
                local_err
            )

            raise HTTPException(
                status_code=400,
                detail=(
                    "Google token verification failed"
                )
            )

    print(
        "Decoded Google Token Data:",
        data
    )

    if not data:

        raise HTTPException(
            status_code=400,
            detail=(
                "Unable to extract Google profile details "
                "from token"
            )
        )

    allowed_client_id = (
        "242260456878-i33gg7lb37j70rk893i4i9svc15ep1pl"
        ".apps.googleusercontent.com"
    )

    aud = data.get("aud")
    azp = data.get("azp")

    aud_valid = False

    if isinstance(aud, list):

        aud_valid = (
            allowed_client_id in aud
        )

    elif isinstance(aud, str):

        aud_valid = (
            aud.strip()
            == allowed_client_id.strip()
        )

    if not aud_valid and isinstance(azp, str):

        aud_valid = (
            azp.strip()
            == allowed_client_id.strip()
        )

    if not aud_valid:

        print(
            ">>> [CLIENT ID ERROR] "
            f"Expected: {allowed_client_id} | "
            f"Token aud: {aud} | "
            f"Token azp: {azp}"
        )

        raise HTTPException(
            status_code=401,
            detail="Invalid Google Client ID"
        )
        
    email = data.get("email")

    name = data.get(
        "name",
        "Google User"
    )

    email_verified = data.get(
        "email_verified"
    )

    if not email:

        raise HTTPException(
            status_code=400,
            detail=(
                "Email field is missing "
                "in Google token payload"
            )
        )

    if str(email_verified).lower() != "true":

        raise HTTPException(
            status_code=400,
            detail="Google email is not verified"
        )

    email = email.strip().lower()

    role = payload.get(
        "role",
        "user"
    )

    role = str(role).strip().lower()

    if role not in ["user", "manager"]:

        raise HTTPException(
            status_code=400,
            detail="Invalid role selected"
        )

    print(
        f">>> GOOGLE LOGIN | "
        f"Email: {email} | "
        f"Selected Role: {role}"
    )

    db_users = load_users()

    found_user = None

    for u in db_users:

        existing_email = (
            str(u.get("email", ""))
            .strip()
            .lower()
        )

        if existing_email != email:
            continue

        existing_role = str(
            u.get("role", "user")
        ).strip().lower()

        print(
            f">>> EXISTING ACCOUNT | "
            f"Email: {email} | "
            f"Existing Role: {existing_role} | "
            f"Selected Role: {role}"
        )
        
        if existing_role == "manager":

            if role == "manager":

                # Existing manager can login
                found_user = u

                break

            else:

                # Manager email cannot login as candidate
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "This email is already registered "
                        "as a recruiter"
                    )
                )


        elif existing_role == "user":

            if role == "user":

                # Existing candidate can login
                found_user = u

                break

            else:

                # User email cannot become recruiter
                raise HTTPException(
                    status_code=400,
                    detail="Email already exists"
                )
        elif existing_role == "admin":

            found_user = u

            break
        else:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Existing account has an invalid role"
                )
            )

    if not found_user:

        print(
            f">>> NEW GOOGLE ACCOUNT | "
            f"Email: {email} | "
            f"Creating Role: {role}"
        )

        new_user = {
            "name": name,
            "email": email,
            "password": "google-oauth-managed-password",
            "role": role
        }

        db_users.append(
            new_user
        )

        save_users(
            db_users
        )

        found_user = new_user

        print(
            f">>> NEW ACCOUNT CREATED | "
            f"Email: {email} | "
            f"Role: {role}"
        )

    access_token = create_access_token({
        "sub": found_user["email"]
    })

    print(
        f">>> GOOGLE LOGIN SUCCESS | "
        f"Email: {found_user['email']} | "
        f"Role: {found_user['role']}"
    )

    return {
        "message": "Google Authentication Successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "name": found_user["name"],
            "email": found_user["email"],
            "role": found_user["role"]
        }
    }
