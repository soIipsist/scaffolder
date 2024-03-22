from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class PostSchema(BaseModel):
    title: str
    content: str
    owner_id: int

    class Config:
        from_attributes = True
