from sqlmodel import Session, select
from app.database.models import User
from collections.abc import Sequence
from app.schemas.user import UserCreate,UserUpdate
from datetime import datetime,timezone

def get_user(session: Session, user_id: int)->User|None:
    return session.get(User, user_id)


def get_users(session: Session)->Sequence[User]:
    statement=select(User)
    return session.exec(statement).all()


def create_user(session: Session, user_data: UserCreate)-> User:

    user = User.model_validate(user_data)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user

def update_user(session: Session, db_user: User, user_data:UserUpdate)->User:
    update_data=user_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)

    db_user.updated_at= datetime.now(timezone.utc)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

def delete_user(session: Session, db_user: User)->None:

    session.delete(db_user)
    session.commit()