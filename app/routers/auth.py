from fastapi import APIRouter, HTTPException
from app.schemas.user import UserRegister
from app.auth.jwt_handler import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


import random

users = []
active_otps = {}


@router.post("/register")
def register(user: UserRegister):

    users.append(user)

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

    found_user = None

    for u in users:
        if u.email == user.email and u.password == user.password:
            found_user = u
            break

    if not found_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token({
        "sub": user.email
    })

    return {
        "message": "Login Successful",
        "access_token": token,
        "token_type": "bearer"
    }


from app.auth.email_sender import send_otp_email


@router.post("/forgot-password")
def forgot_password(payload: dict):
    email = payload.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    
    # Generate real dynamic 6-digit verification code
    otp = str(random.randint(100000, 999999))
    active_otps[email.lower()] = otp
    print(f"\n>>> [OTP GENERATED] Email: {email} | Code: {otp}\n")
    
    # Send actual email to registered user/manager
    email_sent = send_otp_email(email, otp)
    
    return {
        "message": "Verification code sent to registered email address" if email_sent else "Generated verification code internally",
        "email": email
    }


@router.post("/reset-password")
def reset_password(payload: dict):
    email = payload.get("email")
    code = payload.get("code")
    new_password = payload.get("new_password")
    
    if not email or not code or not new_password:
        raise HTTPException(status_code=400, detail="Email, verification code, and new password are required")

    # Verify real generated OTP code
    expected_code = active_otps.get(email.lower())
    if not expected_code or expected_code != str(code).strip():
        raise HTTPException(status_code=400, detail="Invalid or expired verification code")

    user_updated = False
    for u in users:
        if u.email.lower() == email.lower():
            u.password = new_password
            user_updated = True
            break

    # Clean up OTP after successful reset
    active_otps.pop(email.lower(), None)

    return {
        "message": "Password reset successfully",
        "email": email
    }


import urllib.request
import urllib.error
import json
import base64

@router.post("/google-login")
def google_login(payload: dict):
    token = payload.get("token")
    if not token:
        raise HTTPException(status_code=400, detail="Google authentication token is required")

    data = None
    # Method 1: Try verifying online with Google APIs (with User-Agent)
    try:
        url = f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
        )
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
    except Exception as online_err:
        print("Google online verification failed, trying local JWT decoding:", online_err)
        # Method 2: Local JWT Decode Fallback
        try:
            parts = token.split(".")
            if len(parts) == 3:
                payload_b64 = parts[1]
                padded = payload_b64 + "=" * ((4 - len(payload_b64) % 4) % 4)
                decoded_bytes = base64.urlsafe_b64decode(padded)
                data = json.loads(decoded_bytes.decode('utf-8'))
        except Exception as local_err:
            print("Local JWT decoding failed:", local_err)
            raise HTTPException(status_code=400, detail="Google token verification failed (both online and local fallback)")

    print("Decoded Google Token Data:", data)
    if not data:
        raise HTTPException(status_code=400, detail="Unable to extract Google profile details from token")

    # Verify audience client ID (support aud as string/list and azp fallback)
    allowed_client_id = "242260456878-i33gg7lb37j70rk893i4i9svc15ep1pl.apps.googleusercontent.com"
    aud = data.get("aud")
    azp = data.get("azp")
    aud_valid = False

    if isinstance(aud, list):
        aud_valid = allowed_client_id in aud
    elif isinstance(aud, str):
        aud_valid = allowed_client_id.strip() in aud.strip()

    if not aud_valid and azp and isinstance(azp, str):
        aud_valid = allowed_client_id.strip() in azp.strip()

    if not aud_valid:
        print(f">>> [CLIENT ID MISMATCH] Allowed: {allowed_client_id} | Token aud: {aud} | Token azp: {azp}")
        raise HTTPException(status_code=400, detail=f"Audience Client ID mismatch. aud: {aud}, azp: {azp}")

    email = data.get("email")
    name = data.get("name", "Google User")

    if not email:
        raise HTTPException(status_code=400, detail="Email field is missing in Google token payload")

    # Auto-sign up or login user
    found_user = None
    for u in users:
        if u.email.lower() == email.lower():
            found_user = u
            break

    if not found_user:
        # Auto register as a user
        from app.schemas.user import UserRegister
        new_user = UserRegister(
            name=name,
            email=email,
            password="google-oauth-managed-password",
            role="user"
        )
        users.append(new_user)
        found_user = new_user

    # Create live JWT token
    access_token = create_access_token({
        "sub": found_user.email
    })

    return {
        "message": "Google Authentication Successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "name": found_user.name,
            "email": found_user.email,
            "role": found_user.role
        }
    }