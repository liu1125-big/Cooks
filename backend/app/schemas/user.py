from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    nickname: str
    avatar: str | None = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    username: str | None = None
    nickname: str | None = None
    avatar: str | None = None


class UserResponse(UserBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True