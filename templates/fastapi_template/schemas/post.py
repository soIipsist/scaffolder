from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class Post(BaseModel):
    content:str