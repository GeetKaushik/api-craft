from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.auth_dependencies import get_current_user
from app.database.dependencies import get_session
from app.database.models import User
from app.schemas.user import UserUpdate, UserResponse
from app.services import user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


# Get the logged-in user's profile.
@router.get("/", response_model=UserResponse)
def get_my_user(
    current_user: User = Depends(get_current_user),
):
    return current_user


# Get a user by ID, but only allow access to your own account.
@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    user = user_service.get_user(session, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


# Update your own profile.
@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    if user_data.is_active is not None:
        raise HTTPException(
            status_code=400,
            detail="You cannot change your account status",
        )

    user = user_service.get_user(session, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user_service.update_user(
        session,
        user,
        user_data,
    )


# Delete your own account.
@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    user = user_service.get_user(session, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    user_service.delete_user(session, user)

    return {"message": "User deleted successfully"}
