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
import json

@router.post("/google-login")
def google_login(payload: dict):
    token = payload.get("token")
    if not token:
        raise HTTPException(status_code=400, detail="Google authentication token is required")

    try:
        # Request Google endpoint to verify ID Token integrity
        url = f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        # Verify audience client ID
        aud = data.get("aud")
        if aud != "242260456878-i33gg7lb37j70rk893i4i9svc15ep1pl.apps.googleusercontent.com":
            raise HTTPException(status_code=400, detail="Audience client ID mismatch")

        email = data.get("email")
        name = data.get("name", "Google User")

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
    except Exception as e:
        print("Google token verification failed:", e)
        raise HTTPException(status_code=400, detail="Google authentication failed server verification")