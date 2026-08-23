#SQL Model classes(Defines tables)
from typing import Optional
from datetime import datetime
from sqlmodel import Field,SQLModel
from pydantic import EmailStr
# SQLModel: Connects Python code straight to a SQL database while checking data rules.
class User(SQLModel,table=True):
    id:Optional[int]=Field(default=None,primary_key=True)
    name: str = Field(
        min_length=2,
        max_length=100,
        index=True
    )
    email:EmailStr= Field(
        max_length=150,
        unique=True,
        index=True
    )
    
    phone: str | None = Field(
        default=None,
        max_length=15
    )

    is_active: bool = Field(
        default=True
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow
    )