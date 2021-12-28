from fastapi import APIRouter, Depends, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from schemas.user_schema import UserCreateSchema, UserUpdateSchema
from views.user_view import UserView

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/')
async def get_all_users():
    return UserView.get_all()


@router.get('/{user_id}')
async def get_user(user_id: int):
    return UserView.get(user_id)


@router.post('/')
async def create_user(user: UserCreateSchema):
    return UserView.create(user)


@router.post('/token')
async def get_access_token(credentials: OAuth2PasswordRequestForm = Depends()):
    return UserView.token(credentials.username, credentials.password)


@router.put('/')
async def update_user(user: UserUpdateSchema):
    return UserView.update(user)


@router.delete('/{user_id}')
async def delete_user(
        user_id: int,
        token: str = Depends(OAuth2PasswordBearer('users/token')),
):
    return UserView.delete(user_id)
