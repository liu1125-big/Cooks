from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    nickname: str


class UserCreate(UserBase):
    password: str
    role: str = "user"


class UserUpdate(BaseModel):
    username: str | None = None
    nickname: str | None = None
    password: str | None = None
    role: str | None = None


class UserResponse(UserBase):
    id: int
    role: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: str | None = None