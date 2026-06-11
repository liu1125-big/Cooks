from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, func
from app.database.base import Base


class Dish(Base):
    __tablename__ = "dish"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    name = Column(String(100), nullable=False)
    difficulty = Column(Integer, default=1)
    favorite = Column(Boolean, default=False)
    enabled = Column(Boolean, default=True)
    remark = Column(Text, nullable=True)
    image_url = Column(String(255), nullable=True)
    created_by = Column(Integer, ForeignKey("user.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())