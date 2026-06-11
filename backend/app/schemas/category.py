from datetime import datetime
from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    sort: int = 0
    enabled: bool = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = None
    sort: int | None = None
    enabled: bool | None = None


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True