from sqlalchemy import Column, Integer, String
from app.database.base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    nickname = Column(String(50), nullable=False)
    role = Column(String(20), default="user")