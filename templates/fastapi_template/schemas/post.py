from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostSchema(BaseModel):
    id:Optional[int]
    title:str
    content:str

    class Config:
        orm_mode = True