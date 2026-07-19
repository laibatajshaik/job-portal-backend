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