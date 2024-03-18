from fastapi import APIRouter, Depends, status
from requests import Session
from models.post import PostModel
from schemas.post import PostSchema
import os
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)
from database import *

router = APIRouter(prefix='/posts')

@router.get('/{post_id}')
async def get_post(post_id:str):
    return {"message": post_id}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostSchema)
def create_post(post: PostSchema, db: Session = Depends(get_db)):

    new_post = PostModel(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
