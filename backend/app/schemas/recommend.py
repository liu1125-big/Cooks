from pydantic import BaseModel


class RecommendDishResponse(BaseModel):
    id: int
    name: str
    category: str

    class Config:
        from_attributes = True