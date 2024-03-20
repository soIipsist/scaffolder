from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from requests import Session
from fastapi_template.models.user import UserModel
from fastapi_template.schemas.user import UserIn, UserOut
import os
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)
from database import *
from fastapi_template.utils import hash_password

router = APIRouter(prefix='/users')

def get_user_query(user_id:str, db:Session = Depends(get_db)):
    return db.query(UserModel).filter(UserModel.id == user_id)
    

@router.get('/', response_model=List[UserOut])
async def get_users(db:Session = Depends(get_db)):
    users = db.query(UserModel)
    return users

@router.get('/{user_id}', response_model=UserOut)
def get_user(user_id:str, db: Session = Depends(get_db)):
    user = get_user_query(user_id, db).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {user_id} does not exist")

    return user


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


@router.put("/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id:str, updated_user:UserIn, db: Session = Depends(get_db)):
    user_query = get_user_query(user_id, db)
    user = user_query.first()
    if user:
        user_query.update(updated_user.model_dump(), synchronize_session=False)
        db.commit()
        return user_id
    
    raise HTTPException(status_code=404)


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id:str, db: Session = Depends(get_db)):
    user_query = get_user_query(user_id, db)

    user = user_query.first()

    if user:
        user_query.delete(synchronize_session=False)
        db.commit()
        return user_id
    
    raise HTTPException(status_code=404)