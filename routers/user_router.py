from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from models.user_model import User
from permissions import Permission, admin_acl
from schemas.user_schema import UserCreateSchema, UserUpdateSchema
from utils.user_util import UserUtil
from views.user_view import UserView

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/')
async def get_all_users(
        user: User = Permission('view', admin_acl)
):
    return UserView.get_all()


@router.get('/{user_id}')
async def get_user(
        user_id: int,
        user: User = Permission('view', UserUtil.get_by_id)
):
    return UserView.get(user.id)


@router.post('/')
async def create_user(user: UserCreateSchema):
    return UserView.create(user)


@router.post('/token')
async def get_access_token(credentials: OAuth2PasswordRequestForm = Depends()):
    return UserView.token(credentials.username, credentials.password)


@router.put('/{user_id}')
async def update_user(
        user_id: int,
        data: UserUpdateSchema,
        user=Permission('edit', UserUtil.get_by_id)
):
    return UserView.update(user_id, data)


@router.delete('/{user_id}')
async def delete_user(
        user_id: int,
        user: User = Permission('delete', UserUtil.get_by_id)
):
    return UserView.delete(user_id)
