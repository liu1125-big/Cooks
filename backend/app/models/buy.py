from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from app.database.base import Base


class Buy(Base):
    """食材采购表"""
    __tablename__ = "buy"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    number = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)