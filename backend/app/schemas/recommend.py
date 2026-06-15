from typing import Optional
from pydantic import BaseModel


class RecommendDishResponse(BaseModel):
    id: int
    name: str
    category: str
    remark: Optional[str] = None

    class Config:
        from_attributes = True