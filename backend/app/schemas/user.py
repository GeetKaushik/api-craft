from sqlmodel import SQLModel
from pydantic import  BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserCreate(SQLModel):
    name: str = Field(
        min_length=2,
        max_length=100
    )
    email: EmailStr
    phone: Optional[str] = Field(
        default=None,
        max_length=15
    )

class UserUpdate(SQLModel):
    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    email: Optional[EmailStr] = None

    phone: Optional[str] = Field(
        default=None,
        max_length=15
    )

    is_active: Optional[bool] = None

class UserResponse(BaseModel):

    id: int
    name: str
    email: EmailStr
    phone: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime