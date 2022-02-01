from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_permissions import has_permission, permission_exception

from core.dependencies import get_user_repository
from core.exceptions import ObjectAlreadyExistsError, ObjectDoesNotExists
from core.permissions import ADMIN_ACL, Permission, get_user_principles
from repository.user import UserRepository
from schemas.user import User, UserCreate, UsersList, UserUpdate
from utils.user_auth import authenticate, create_access_token

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/')
async def get_all_users(
        acls: List = Permission('view', ADMIN_ACL),
        repository: UserRepository = Depends(get_user_repository)
):
    users = await repository.get_all_users()
    return UsersList(
        users=[User.from_orm(i) for i in users]
    )


@router.get('/{user_id}')
async def get_user(
        user_id: int,
        principles: List = Depends(get_user_principles),
        repository: UserRepository = Depends(get_user_repository),
):
    user = await repository.get_by_id(user_id)
    if user and has_permission(principles, 'view', user):
        return User.from_orm(user)
    raise HTTPException(status.HTTP_400_BAD_REQUEST)


@router.post('/')
async def create_user(
        data: UserCreate,
        repository: UserRepository = Depends(get_user_repository)
):
    try:
        user = await repository.create_user(data)
        return User.from_orm(user)
    except ObjectAlreadyExistsError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=e.message)


@router.post('/token')
async def get_access_token(credentials: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate(credentials.username, credentials.password)
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
        principles: List = Depends(get_user_principles),
        repository: UserRepository = Depends(get_user_repository),
):
    try:
        user = await repository.get_by_id(user_id)
        if not has_permission(principles, 'edit', user):
            raise permission_exception

        user = await repository.update_user(user, data)
        return User.from_orm(user)
    except ObjectDoesNotExists as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=e.message)
    except ObjectAlreadyExistsError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=e.message)


@router.delete('/{user_id}')
async def delete_user(
        user_id: int,
        principals: List = Depends(get_user_principles),
        repository: UserRepository = Depends(get_user_repository)
):
    try:
        user = await repository.get_by_id(user_id)
    except ObjectDoesNotExists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    if not has_permission(principals, 'delete', user):
        raise permission_exception

    await repository.delete_user(user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
