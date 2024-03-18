from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserIn(BaseModel):
    name:str
    surname:str
    username:str
    password: str

class UserOut(BaseModel):
    name:str
    surname:str
    username:str