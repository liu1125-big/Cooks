from datetime import datetime
from pydantic import BaseModel


class DishBase(BaseModel):
    name: str
    category_id: int
    difficulty: int = 1
    favorite: bool = False
    enabled: bool = True
    remark: str | None = None
    image_url: str | None = None


class DishCreate(DishBase):
    created_by: int | None = None


class DishUpdate(BaseModel):
    name: str | None = None
    category_id: int | None = None
    difficulty: int | None = None
    favorite: bool | None = None
    enabled: bool | None = None
    remark: str | None = None
    image_url: str | None = None


class DishResponse(DishBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True