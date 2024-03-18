from fastapi import APIRouter, Depends, status
from requests import Session
from models.user import User
from schemas.user import UserIn, UserOut
import os
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)
from database import *

router = APIRouter(prefix='/users')

@router.get('/{user_id}')
async def get_user(user_id:str):
    return {"message": user_id}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserIn, db: Session = Depends(get_db)):

    # hash the password
    # hashed_password = utils.hash(user.password)
    # user.password = 'password'

    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
