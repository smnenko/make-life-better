from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from core.permissions import ADMIN_ACL, Permission
from exceptions.user import UserDoesNotExists, UserUniqueConstraintException
from models.user import User as UserDB
from crud.user import UserOrm
from schemas.user import User, UserCreate, UsersList, UserUpdate
from utils.user_auth import authenticate, create_access_token

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/')
async def get_all_users(
        acls=Permission('view', ADMIN_ACL)
):
    print(acls)
    return UsersList(
        users=[User.from_orm(i) for i in UserOrm.get_all_users()]
    )


@router.get('/{user_id}')
async def get_user(
        user_id: int,
        user: UserDB = Permission('view', UserOrm.get_by_id)
):
    if user:
        return User.from_orm(user)
    raise HTTPException(status.HTTP_400_BAD_REQUEST)


@router.post('/')
async def create_user(user: UserCreate):
    try:
        user = UserOrm.create_user(
            email=user.email,
            username=user.username,
            password=user.password
        )
        return User.from_orm(user)
    except UserUniqueConstraintException as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=e.message)


@router.post('/token')
async def get_access_token(credentials: OAuth2PasswordRequestForm = Depends()):
    user = authenticate(credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            'Username or password is invalid'
        )

    access_token = create_access_token({'username': credentials.username})
    return {'access_token': access_token, 'token_type': 'Bearer'}


@router.put('/{user_id}')
async def update_user(
        user_id: int,
        data: UserUpdate,
        user: UserDB = Permission('edit', UserOrm.get_by_id)
):
    try:
        user = UserOrm.update_user(user, data)
        return User.from_orm(user)
    except UserUniqueConstraintException as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=e.message)


@router.delete('/{user_id}')
async def delete_user(
        user_id: int,
        user: User = Permission('delete', UserOrm.get_by_id)
):
    try:
        UserOrm.delete_user(user)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except UserDoesNotExists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
