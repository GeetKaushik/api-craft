from pydantic import BaseModel, EmailStr, Field


# RegisterRequest validates the information submitted when someone creates an account.
class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    phone: str | None = Field(default=None, max_length=15)


# LoginRequest validates login credentials.
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


# TokenResponse defines the format returned after successful login.
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
