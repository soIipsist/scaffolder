from fastapi import APIRouter, Depends, status
from requests import Session
from models.user import UserModel
from schemas.user import UserIn, UserOut
import os
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)
from database import *
from utils import hash_password

router = APIRouter(prefix='/users')

@router.get('/{user_id}')
async def get_user(user_id:str):
    return {"message": user_id}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserIn, db: Session = Depends(get_db)):

    # hash the password
    hashed_password = hash_password(user.password)
    new_user = UserModel(**user.model_dump())
    new_user.password = hashed_password

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
