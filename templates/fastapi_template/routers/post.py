from fastapi import APIRouter, Depends, HTTPException, status
from psycopg2 import IntegrityError
from requests import Session
from models.post import PostModel
from schemas.post import PostSchema
import os
from psycopg2.errors import ForeignKeyViolation
from sqlalchemy.exc import IntegrityError as SQLAlchemyIntegrityError

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)
from database import *

router = APIRouter(prefix="/posts")


@router.get("/{post_id}", response_model=PostSchema)
async def get_post(post_id: str, db: Session = Depends(get_db)):
    post = db.query(PostModel).filter(PostModel.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {post_id} does not exist",
        )
    return post


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(post: PostSchema, db: Session = Depends(get_db)):

    try:
        new_post = PostModel(**post.model_dump())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post

    except Exception as e:
        print(type(e))
        if isinstance(e, ForeignKeyViolation):
            raise HTTPException(
                status_code=400, detail="Foreign key constraint violated"
            )
        elif isinstance(e, SQLAlchemyIntegrityError) or isinstance(e, IntegrityError):
            raise HTTPException(status_code=400, detail="Integrity error.")
        else:
            raise HTTPException(status_code=500, detail="Internal Server Error")
