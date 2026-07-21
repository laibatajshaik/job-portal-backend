from fastapi import APIRouter, HTTPException
from app.schemas.user import UserRegister
from app.auth.jwt_handler import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


users = []


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
    return {
        "message": "Verification code sent to registered email",
        "email": email
    }


@router.post("/reset-password")
def reset_password(payload: dict):
    email = payload.get("email")
    new_password = payload.get("new_password")
    if not email or not new_password:
        raise HTTPException(status_code=400, detail="Email and new password are required")

    user_updated = False
    for u in users:
        if u.email.lower() == email.lower():
            u.password = new_password
            user_updated = True
            break

    return {
        "message": "Password reset successfully",
        "email": email
    }