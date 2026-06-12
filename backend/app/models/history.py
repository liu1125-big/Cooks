from sqlalchemy import Column, Integer, DateTime, ForeignKey, func
from app.database.base import Base


class History(Base):
    """历史记录表"""
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    dish_id = Column(Integer, ForeignKey("dish.id"), nullable=False)
    time = Column(DateTime, server_default=func.now())