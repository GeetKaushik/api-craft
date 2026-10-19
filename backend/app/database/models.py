# SQL Model classes(Defines tables)
from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel
from pydantic import EmailStr
from sqlalchemy import Column, Text, UniqueConstraint


# SQLModel: Connects Python code straight to a SQL database while checking data rules.
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(min_length=2, max_length=100, index=True)
    email: EmailStr = Field(max_length=150, unique=True, index=True)

    hashed_password: Optional[str] = Field(default=None, max_length=255)

    phone: str | None = Field(default=None, max_length=15)

    is_active: bool = Field(default=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(default_factory=datetime.utcnow)


class GeneratedAPI(SQLModel, table=True):
    __tablename__ = "generated_api"

    __table_args__ = (
        UniqueConstraint(
            "owner_id",
            "resource_name",
            name="uq_generated_api_owner_resource",
        ),
    )

    id: int | None = Field(default=None, primary_key=True)

    owner_id: int = Field(
        foreign_key="user.id",
        index=True,
    )

    resource_name: str = Field(max_length=100)

    table_name: str = Field(
        max_length=128,
        unique=True,
    )

    description: str | None = Field(default=None, max_length=500)

    api_schema_json: str = Field(
        sa_column=Column("schema_json", Text, nullable=False),
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
    )
    
    is_archived: bool = Field(default=False, nullable=False)

