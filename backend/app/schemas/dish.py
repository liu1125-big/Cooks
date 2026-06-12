from datetime import datetime
from pydantic import BaseModel


class DishBase(BaseModel):
    category: str
    name: str
    remark: str | None = None


class DishCreate(DishBase):
    pass


class DishUpdate(BaseModel):
    category: str | None = None
    name: str | None = None
    remark: str | None = None


class DishResponse(DishBase):
    id: int

    class Config:
        from_attributes = True