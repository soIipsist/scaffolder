from typing import Optional
from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text

class UserModel(Base):
    __tablename__ = "Users"

    id = Column(Integer,primary_key=True, autoincrement=True)
    name = Column(String,nullable=False)
    surname = Column(String,nullable=False)
    username = Column(String,nullable=False)
    password = Column(String, nullable=False)