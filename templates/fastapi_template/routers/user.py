from fastapi import APIRouter
from models.user import User as UserModel
from schemas.user import User as UserSchema

router = APIRouter(prefix='/users')

@router.get('/{user_id}')
async def get_user(user_id:str):
    return {"message": user_id}


@router.post('/')
async def create_user(user:UserSchema):
    user_model = UserModel(**user.model_dump())
    return vars(user_model)
