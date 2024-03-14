from typing import Optional
from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text

class User(Base):
    __tablename__ = "User"

    id = Column(Integer,primary_key=True,nullable=False)
    name = Column(String,nullable=False)
    surname = Column(String,nullable=False)
    username = Column(String,nullable=False)
    password = Column(String, nullable=False)