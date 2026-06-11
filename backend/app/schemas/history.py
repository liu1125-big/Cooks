from datetime import datetime
from pydantic import BaseModel


class HistoryBase(BaseModel):
    dish_id: int
    selected_by: int | None = None
    selected_method: str
    comment: str | None = None


class HistoryCreate(HistoryBase):
    pass


class HistoryResponse(HistoryBase):
    id: int
    created_at: datetime | None = None

    class Config:
        from_attributes = True