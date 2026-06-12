from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from app.database.base import Base


class Favorite(Base):
    """用户收藏表"""
    __tablename__ = "favorite"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    dish_id = Column(Integer, ForeignKey("dish.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint('user_id', 'dish_id', name='uq_user_favorite_dish'),
    )