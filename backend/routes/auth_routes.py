from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

from authentication.auth import (
    user_exists,
    create_user,
    get_user_by_email,
    verify_password
)


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


# ============================================================
# REQUEST MODELS
# ============================================================

class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ============================================================
# SIGNUP
# ============================================================

@router.post("/signup")
def signup(data: SignupRequest):

    username = data.username.strip()
    email = str(data.email).strip().lower()
    password = data.password
    confirm_password = data.confirm_password

    # --------------------------------------------------------
    # Validate username
    # --------------------------------------------------------

    if not username:
        raise HTTPException(
            status_code=400,
            detail="Username is required."
        )

    if len(username) < 3:
        raise HTTPException(
            status_code=400,
            detail="Username must contain at least 3 characters."
        )

    # --------------------------------------------------------
    # Validate password
    # --------------------------------------------------------

    if len(password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least 8 characters."
        )

    if password != confirm_password:
        raise HTTPException(
            status_code=400,
            detail="Passwords do not match."
        )

    # --------------------------------------------------------
    # Check existing user
    # --------------------------------------------------------

    if user_exists(email):

        raise HTTPException(
            status_code=409,
            detail="An account with this email already exists."
        )

    # --------------------------------------------------------
    # Create user
    # --------------------------------------------------------

    success = create_user(
        username,
        email,
        password
    )

    if not success:

        raise HTTPException(
            status_code=500,
            detail="Unable to create account. Please try again."
        )

    return {
        "success": True,
        "message": "Account created successfully."
    }


# ============================================================
# LOGIN
# ============================================================

@router.post("/login")
def login(data: LoginRequest):

    email = str(data.email).strip().lower()
    password = data.password

    # --------------------------------------------------------
    # Validate fields
    # --------------------------------------------------------

    if not email or not password:

        raise HTTPException(
            status_code=400,
            detail="Email and password are required."
        )

    # --------------------------------------------------------
    # Find user
    # --------------------------------------------------------

    user = get_user_by_email(email)

    if user is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    # --------------------------------------------------------
    # Verify password
    # --------------------------------------------------------

    if not verify_password(
        password,
        user["password_hash"]
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    # --------------------------------------------------------
    # Successful login
    # --------------------------------------------------------

    return {
        "success": True,
        "message": "Login successful.",
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"]
        }
    }