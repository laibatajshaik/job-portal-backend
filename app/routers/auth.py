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


@router.post("/forgot-password")
def forgot_password(payload: dict):
    email = payload.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    
    # Generate real dynamic 6-digit verification code
    otp = str(random.randint(100000, 999999))
    active_otps[email.lower()] = otp
    print(f"\n>>> [OTP GENERATED] Email: {email} | Code: {otp}\n")
    
    return {
        "message": "Verification code generated successfully",
        "email": email,
        "code": otp
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