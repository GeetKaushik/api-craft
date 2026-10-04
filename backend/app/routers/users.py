from fastapi import APIRouter,Depends,HTTPException
from sqlmodel import Session,select
from datetime import datetime, timezone
from app.database.dependencies import get_session
from app.database.models import User
from app.schemas.user import UserCreate,UserUpdate,UserResponse
from app.services import user_service

router=APIRouter(prefix="/users",
                 tags=["Users"])

# @router.get("/")
# def home(session:Session):
#     return{"message":"Users Router Working"}

# To create a new user
@router.post(
        "/",
        response_model=UserResponse,
        status_code=201)
def create_user(
    user_data:UserCreate,
    session:Session=Depends(get_session)
):
    return user_service.create_user(
        session,
        user_data
    )

# To get all the users
@router.get("/",response_model=list[UserResponse])
def get_users(session:Session=Depends(get_session)):# gives the endpoint  database session
    # statement=select(User)# SQL Query
    # users=session.exec(statement).all() #Execute the query using the db session
    return user_service.get_users(session)


# To get one user at a time
@router.get("/{user_id}",response_model=UserResponse)
def get_user(
    user_id:int,# User id should be integer
    session:Session=Depends(get_session)
):
    # The User is the model and id should be the primary key of the model
    # user=session.get(User,id)#To find the record in user table whole primary key is user_id
    user=user_service.get_user(
        session,
        user_id
    )
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return user

@router.put("/{user_id}",response_model=UserResponse)
def update_user(
    user_id:int,
    user_data:UserUpdate,
    session:Session=Depends(get_session)
)->User:
    user = user_service.get_user(
        session,
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user_service.update_user(
        session,
        user,
        user_data
    )
    
    # db_user=session.get(User,user_id)
    # if not db_user:
    #     return{"message":"User not found"}
    # db_user.name=user.name
    # db_user.email=user.email
    # db_user.phone=user.phone
    # db_user.updated_at = datetime.now(timezone.utc)
    # session.add(db_user)
    # session.commit()
    # session.refresh(db_user)
    # return db_user

@router.delete("/{user_id}")
def delete_user(
    user_id:int,
    session:Session=Depends(get_session)
):
    # user=session.get(User,user_id)
    db_user = user_service.get_user(
        session,
        user_id
    )
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    user_service.delete_user(
        session,
        db_user
    )
    # session.delete(user)
    # session.commit()
    return{"message":"User deleted successfully"}