from fastapi import APIRouter

from schemas.user import UserCreateSchema, UserUpdateSchema
from utils.user import UserUtil


router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/')
async def get_all_users():
    return UserUtil().get_all()


@router.get('/{user_id}')
async def get_user_by_id(user_id: int):
    return UserUtil().get_by_id(user_id)


@router.post('/')
async def create_user(user: UserCreateSchema):
    return UserUtil().create_user(user)


@router.put('/')
async def update_user(user: UserUpdateSchema):
    return UserUtil().update_user(user)


@router.delete('/{user_id}')
async def delete_user_by_id(user_id: int):
    return UserUtil().delete_by_id(user_id)
