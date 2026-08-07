from fastapi import APIRouter, HTTPException
from app.schemas.user import UserRegister
from app.auth.jwt_handler import create_access_token
from app.db import load_users, save_users
from app.auth.email_sender import send_otp_email

import random
import os
import smtplib
import urllib.request
import json
import base64

from email.mime.text import MIMEText


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

active_otps = {}


# =========================================================
# REGISTER
# =========================================================

@router.post("/register")
def register(user: UserRegister):

    db_users = load_users()

    email = user.email.strip().lower()

    for u in db_users:

        existing_email = str(
            u.get("email", "")
        ).strip().lower()

        if existing_email == email:

            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

    new_user = {
        "name": user.name,
        "email": email,
        "password": user.password,
        "role": user.role
    }

    db_users.append(new_user)

    save_users(db_users)

    token = create_access_token({
        "sub": email
    })

    return {
        "message": "User Registered Successfully",
        "access_token": token,
        "token_type": "bearer"
    }


# =========================================================
# NORMAL LOGIN
# =========================================================

@router.post("/login")
def login(user: UserRegister):

    db_users = load_users()

    email = user.email.strip().lower()

    found_user = None

    for u in db_users:

        existing_email = str(
            u.get("email", "")
        ).strip().lower()

        if (
            existing_email == email
            and u.get("password") == user.password
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


# =========================================================
# TEST EMAIL STATUS
# =========================================================

@router.get("/test-email-status")
def test_email_status(to: str):

    res = {}

    # -----------------------------
    # RESEND
    # -----------------------------

    resend_key = os.getenv("RESEND_API_KEY")

    res["resend_key_configured"] = bool(
        resend_key
    )

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
                data=json.dumps(
                    payload
                ).encode("utf-8"),
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

    # -----------------------------
    # BREVO
    # -----------------------------

    brevo_key = os.getenv("BREVO_API_KEY")

    res["brevo_key_configured"] = bool(
        brevo_key
    )

    if brevo_key:

        try:

            url = (
                "https://api.brevo.com/"
                "v3/smtp/email"
            )

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
                data=json.dumps(
                    payload
                ).encode("utf-8"),
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

    # -----------------------------
    # SMTP
    # -----------------------------

    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER")

    smtp_port = int(
        os.getenv(
            "SMTP_PORT",
            "2525"
        )
    )

    if (
        smtp_user
        and smtp_password
        and smtp_server
    ):

        try:

            msg = MIMEText(
                "Test SMTP"
            )

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
            "SMTP credentials not fully "
            "configured in environment"
        )

    return res


# =========================================================
# FORGOT PASSWORD
# =========================================================

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
        random.randint(
            100000,
            999999
        )
    )

    active_otps[email] = otp

    print(
        f"\n>>> [OTP GENERATED] "
        f"Email: {email} | "
        f"Code: {otp}\n"
    )

    email_sent = send_otp_email(
        email,
        otp
    )

    return {
        "message": (
            "Verification code sent to "
            "registered email address"
            if email_sent
            else
            "Generated verification code internally"
        ),
        "email": email
    }


# =========================================================
# RESET PASSWORD
# =========================================================

@router.post("/reset-password")
def reset_password(payload: dict):

    email = payload.get("email")
    code = payload.get("code")
    new_password = payload.get(
        "new_password"
    )

    if (
        not email
        or not code
        or not new_password
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                "Email, verification code, "
                "and new password are required"
            )
        )

    email = email.strip().lower()

    expected_code = active_otps.get(
        email
    )

    if (
        not expected_code
        or expected_code != str(code).strip()
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid or expired "
                "verification code"
            )
        )

    db_users = load_users()

    user_updated = False

    for u in db_users:

        existing_email = str(
            u.get("email", "")
        ).strip().lower()

        if existing_email == email:

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


# =========================================================
# GOOGLE OAUTH LOGIN
# =========================================================

@router.post("/google-login")
def google_login(payload: dict):

    # -----------------------------------------------------
    # 1. Get Google token
    # -----------------------------------------------------

    token = payload.get("token")

    if not token:

        raise HTTPException(
            status_code=400,
            detail=(
                "Google authentication "
                "token is required"
            )
        )

    # -----------------------------------------------------
    # 2. Get selected role from frontend
    # -----------------------------------------------------

    selected_role = payload.get(
        "role",
        "user"
    )

    selected_role = str(
        selected_role
    ).strip().lower()

    if selected_role not in [
        "user",
        "manager"
    ]:

        raise HTTPException(
            status_code=400,
            detail="Invalid role selected"
        )

    print(
        f">>> GOOGLE SELECTED ROLE: "
        f"{selected_role}"
    )

    # -----------------------------------------------------
    # 3. Verify Google token
    # -----------------------------------------------------

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
                    "Chrome/120.0.0.0 "
                    "Safari/537.36"
                )
            }
        )

        with urllib.request.urlopen(
            req
        ) as response:

            data = json.loads(
                response.read().decode(
                    "utf-8"
                )
            )

    except Exception as online_error:

        print(
            "Google online verification failed:",
            online_error
        )

        # -------------------------------------------------
        # Fallback JWT payload decoding
        # -------------------------------------------------

        try:

            parts = token.split(".")

            if len(parts) != 3:

                raise ValueError(
                    "Invalid JWT structure"
                )

            payload_b64 = parts[1]

            padded = (
                payload_b64
                + "=" * (
                    (
                        4
                        - len(payload_b64) % 4
                    ) % 4
                )
            )

            decoded_bytes = (
                base64.urlsafe_b64decode(
                    padded
                )
            )

            data = json.loads(
                decoded_bytes.decode(
                    "utf-8"
                )
            )

        except Exception as local_error:

            print(
                "Local JWT decoding failed:",
                local_error
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
                "Unable to extract Google "
                "profile details from token"
            )
        )

    # -----------------------------------------------------
    # 4. Validate Google Client ID
    # -----------------------------------------------------

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

    if not aud_valid:

        if isinstance(
            azp,
            str
        ):

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

    # -----------------------------------------------------
    # 5. Get Google user information
    # -----------------------------------------------------

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

    if str(
        email_verified
    ).lower() != "true":

        raise HTTPException(
            status_code=400,
            detail=(
                "Google email is not verified"
            )
        )

    email = email.strip().lower()

    # -----------------------------------------------------
    # 6. Load existing users
    # -----------------------------------------------------

    db_users = load_users()

    print(
        ">>> TOTAL USERS IN DATABASE:",
        len(db_users)
    )

    found_user = None

    # -----------------------------------------------------
    # 7. Check existing account
    # -----------------------------------------------------

    for u in db_users:

        existing_email = str(
            u.get(
                "email",
                ""
            )
        ).strip().lower()

        if existing_email != email:

            continue

        existing_role = str(
            u.get(
                "role",
                "user"
            )
        ).strip().lower()

        print(
            ">>> EXISTING ACCOUNT FOUND"
        )

        print(
            f">>> Email: {email}"
        )

        print(
            f">>> Existing Role: "
            f"{existing_role}"
        )

        print(
            f">>> Selected Role: "
            f"{selected_role}"
        )

        # =================================================
        # EXISTING USER ACCOUNT
        # =================================================

        if existing_role == "user":

            # User selects Candidate
            if selected_role == "user":

                found_user = u

                print(
                    ">>> EXISTING USER LOGIN ALLOWED"
                )

                break

            # User selects Recruiter
            else:

                print(
                    ">>> USER EMAIL CANNOT "
                    "LOGIN AS RECRUITER"
                )

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Email already exists "
                        "as a candidate"
                    )
                )

        # =================================================
        # EXISTING MANAGER ACCOUNT
        # =================================================

        elif existing_role == "manager":

            # Manager selects Recruiter
            if selected_role == "manager":

                found_user = u

                print(
                    ">>> EXISTING MANAGER "
                    "LOGIN ALLOWED"
                )

                break

            # Manager selects Candidate
            else:

                print(
                    ">>> MANAGER EMAIL CANNOT "
                    "LOGIN AS CANDIDATE"
                )

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "This email is already "
                        "registered as a recruiter"
                    )
                )

        # =================================================
        # EXISTING ADMIN ACCOUNT
        # =================================================

        elif existing_role == "admin":

            found_user = u

            print(
                ">>> EXISTING ADMIN LOGIN"
            )

            break

        # =================================================
        # INVALID ROLE
        # =================================================

        else:

            print(
                ">>> INVALID EXISTING ROLE:",
                existing_role
            )

            raise HTTPException(
                status_code=400,
                detail=(
                    "Existing account has "
                    "an invalid role"
                )
            )

    # -----------------------------------------------------
    # 8. Create NEW Google account
    # -----------------------------------------------------

    if not found_user:

        print(
            ">>> NEW GOOGLE ACCOUNT"
        )

        print(
            f">>> Email: {email}"
        )

        print(
            f">>> Creating Role: "
            f"{selected_role}"
        )

        new_user = {
            "name": name,
            "email": email,
            "password": (
                "google-oauth-managed-password"
            ),
            "role": selected_role
        }

        db_users.append(
            new_user
        )

        save_users(
            db_users
        )

        found_user = new_user

        print(
            ">>> NEW GOOGLE ACCOUNT CREATED"
        )

        print(
            f">>> Email: {email}"
        )

        print(
            f">>> Role: "
            f"{selected_role}"
        )

    # -----------------------------------------------------
    # 9. Create JWT
    # -----------------------------------------------------

    access_token = create_access_token({
        "sub": found_user["email"]
    })

    # -----------------------------------------------------
    # 10. Final role verification
    # -----------------------------------------------------

    final_role = str(
        found_user.get(
            "role",
            "user"
        )
    ).strip().lower()

    print(
        "===================================="
    )

    print(
        ">>> GOOGLE LOGIN SUCCESS"
    )

    print(
        f">>> Email: "
        f"{found_user['email']}"
    )

    print(
        f">>> Selected Role: "
        f"{selected_role}"
    )

    print(
        f">>> Database Role: "
        f"{final_role}"
    )

    print(
        "===================================="
    )

    # -----------------------------------------------------
    # 11. Return user
    # -----------------------------------------------------

    return {
        "message": (
            "Google Authentication Successful"
        ),
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "name": found_user["name"],
            "email": found_user["email"],
            "role": final_role
        }
    }
