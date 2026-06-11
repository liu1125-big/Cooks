from pydantic import BaseModel


class RecommendDishResponse(BaseModel):
    id: int
    name: str
    category_id: int

    class Config:
        from_attributes = True