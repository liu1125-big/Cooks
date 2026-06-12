from sqlalchemy import Column, Integer, DateTime, ForeignKey, func, UniqueConstraint
from app.database.base import Base


class Cart(Base):
    """购物车表"""
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    dish_id = Column(Integer, ForeignKey("dish.id"), nullable=False)
    quantity = Column(Integer, default=1)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint('user_id', 'dish_id', name='uq_user_dish'),
    )