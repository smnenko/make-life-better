from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi_permissions import has_permission, permission_exception

from core.dependencies import get_user_repository
from core.exceptions import ObjectAlreadyExistsError, ObjectDoesNotExists
from core.permissions import get_user_principles
from repository.user import UserRepository
from schemas.user import User, UserCreate, UserUpdate


router = APIRouter(prefix='/users', tags=['Users'])


@router.get(
    path='/',
    response_model=List[User],
    description='Method returns list of users'
)
async def get_all_users(
        principles: List = Depends(get_user_principles),
        repository: UserRepository = Depends(get_user_repository),
):
    users = await repository.get_all_users()
    if not all(has_permission(principles, 'view', i) for i in users):
        raise permission_exception
    return users


@router.get(
    path='/{user_id}',
    response_model=User,
    description='Method returns info about requested user'
)
async def get_user(
        user_id: int,
        principles: List = Depends(get_user_principles),
        repository: UserRepository = Depends(get_user_repository),
):
    try:
        user = await repository.get_by_id(user_id)
    except ObjectDoesNotExists:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    if user and has_permission(principles, 'view', user):
        return user
    raise HTTPException(status.HTTP_400_BAD_REQUEST)


@router.post(
    path='/',
    response_model=User,
    description='Method provide user signup and returns user info'
)
async def create_user(
        data: UserCreate,
        repository: UserRepository = Depends(get_user_repository)
):
    try:
        return await repository.create_user(data)
    except ObjectAlreadyExistsError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=e.message)


@router.put(
    path='/{user_id}',
    response_model=User,
    description='Updates whole user model without special fields'
)
async def update_user(
        user_id: int,
        data: UserUpdate,
        principles: List = Depends(get_user_principles),
        repository: UserRepository = Depends(get_user_repository),
):
    try:
        user = await repository.get_by_id(user_id)
    except ObjectDoesNotExists as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=e.message)
    except ObjectAlreadyExistsError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=e.message)
    if not has_permission(principles, 'edit', user):
        raise permission_exception

    return await repository.update_user(user, data)


@router.delete(
    path='/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    description='Method doesn\'t return anything but a status'
)
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
