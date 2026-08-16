from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.user import User

from app.schemas.user import (
    UserLogin,
    UserRegister,
    UserProfileUpdate,
    PasswordUpdate
)

from app.auth.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.auth.dependencies import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# =========================
# REGISTER
# =========================

@router.post("/register")
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully"
    }


# =========================
# LOGIN
# =========================

@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        user.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
        {
            "sub": db_user.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# =========================
# GET PROFILE
# =========================

@router.get("/profile")
def profile(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == current_user
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "name": db_user.name,
        "email": db_user.email
    }


# =========================
# UPDATE PROFILE
# =========================

@router.put("/profile")
def update_profile(
    user_data: UserProfileUpdate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == current_user
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not user_data.name.strip():
        raise HTTPException(
            status_code=400,
            detail="Name cannot be empty"
        )

    db_user.name = user_data.name.strip()

    db.commit()
    db.refresh(db_user)

    return {
        "message": "Profile updated successfully",
        "name": db_user.name,
        "email": db_user.email
    }


# =========================
# CHANGE PASSWORD
# =========================

@router.put("/password")
def update_password(
    password_data: PasswordUpdate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == current_user
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Verify current password
    if not verify_password(
        password_data.current_password,
        db_user.password
    ):
        raise HTTPException(
            status_code=400,
            detail="Current password is incorrect"
        )

    # Validate new password
    if len(password_data.new_password) < 6:
        raise HTTPException(
            status_code=400,
            detail="New password must be at least 6 characters"
        )

    # Don't allow same password
    if verify_password(
        password_data.new_password,
        db_user.password
    ):
        raise HTTPException(
            status_code=400,
            detail="New password must be different from current password"
        )

    # Hash new password
    db_user.password = hash_password(
        password_data.new_password
    )

    db.commit()

    return {
        "message": "Password updated successfully"
    }