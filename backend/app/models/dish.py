from sqlalchemy import Column, Integer, String, Text, func
from app.database.base import Base


class Dish(Base):
    __tablename__ = "dish"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(50), nullable=False)
    name = Column(String(100), nullable=False, unique=True)
    remark = Column(Text, nullable=True)