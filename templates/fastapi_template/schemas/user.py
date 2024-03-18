from pydantic import BaseModel

class User(BaseModel):
    name:str
    surname:str
    username:str