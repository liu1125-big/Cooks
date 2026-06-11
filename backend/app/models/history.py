from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from app.database.base import Base


class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dish_id = Column(Integer, ForeignKey("dish.id"), nullable=False)
    selected_by = Column(Integer, ForeignKey("user.id"), nullable=True)
    selected_method = Column(String(20), nullable=False)
    comment = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())