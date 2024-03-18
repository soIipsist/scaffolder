from fastapi import APIRouter, Depends
from requests import Session
from models.user import User as UserModel
from schemas.user import User as UserSchema
import os
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)
from database import *

router = APIRouter(prefix='/users')

@router.get('/{user_id}')
async def get_user(user_id:str):
    return {"message": user_id}


@router.post('/')
async def create_user(user:UserSchema, db: Session = Depends(get_db)):
    user_model = UserModel(**user.model_dump())

    db.add(user_model)
    db.commit()
    db.refresh(user_model)  # Refresh the model to get the latest data (e.g., auto-generated IDs)
    return user_model.dict()
