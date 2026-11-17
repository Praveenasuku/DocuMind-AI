
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

import jwt
from jwt.exceptions import InvalidTokenError

from database import get_db
from models import User
from schemas import UserCreate, UserResponse, TokenResponse
from services.auth_service import register_user, authenticate_user
from security import create_access_token
from config import settings


# Create router
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# OAuth2 token configuration
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


# ----------------------------------
# 1. USER REGISTRATION
# ----------------------------------

@router.post("/register", response_model=UserResponse)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):

    user = register_user(db, user_data)

    if user is None:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    return user


# ----------------------------------
# 2. USER LOGIN
# ----------------------------------

@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = authenticate_user(
        db,
        form_data.username,
        form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ----------------------------------
# 3. GET CURRENT USER
# ----------------------------------

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:

        # Decode JWT token
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        # Extract user ID
        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user_id = int(user_id)

    except (InvalidTokenError, ValueError, TypeError):
        raise credentials_exception

    # Find user in database
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None or not user.is_active:
        raise credentials_exception

    return user


# ----------------------------------
# 4. PROTECTED PROFILE API
# ----------------------------------

@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):

    return current_user
