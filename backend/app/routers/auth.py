
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database.dependencies import get_session
from app.database.models import User
from app.schemas.auth import (
    RegisterRequest, 
    TokenResponse,
    LoginRequest)
from app.schemas.user import UserResponse
from app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.auth_dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
)
def register_user(
    user_data: RegisterRequest,
    session: Session = Depends(get_session),
):
    # Check whether this email is already registered.
    existing_user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="An account with this email already exists",
        )

    # Hash the password before saving it.
    user = User(
        name=user_data.name,
        email=user_data.email,
        phone=user_data.phone,
        hashed_password=hash_password(user_data.password),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.post("/login",response_model=TokenResponse)
def login_user(
    login_data:LoginRequest,
    session:Session=Depends(get_session),
):
    #Find the user by email.
    user=session.exec(
        select(User).where(User.email==login_data.email)
    ).first()

    # Reject unknown users and accounts without a password.
    if (
        user is None
        or user.hashed_password is None
        or not verify_password(
            login_data.password,
            user.hashed_password,
        )
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="This account is inactive",
        )

    # Generate a signed JWT for this user.
    token = create_access_token(user.id)

    return {
        "access_token": token,
        "token_type": "bearer",
    }

@router.get("/me",response_model=UserResponse)
def get_my_profile(
    current_user:User=Depends(get_current_user),
):
    return current_user