
from sqlalchemy.orm import Session

from models import User
from schemas import UserCreate
from security import hash_password, verify_password


# Register a new user
def register_user(db: Session, user_data: UserCreate):

    # Check whether email already exists
    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_user:
        return None

    # Hash the password
    hashed_password = hash_password(user_data.password)

    # Create new user object
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password
    )

    # Save user in database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Authenticate an existing user
def authenticate_user(db: Session, email: str, password: str):

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    if not user.is_active:
        return None

    return user
