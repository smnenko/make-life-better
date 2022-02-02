from datetime import date
from typing import List, Optional

from fastapi import Depends, HTTPException, status, Response
from fastapi.routing import APIRouter
from fastapi_permissions import has_permission, permission_exception

from core.dependencies import get_calorie_repository
from core.exceptions import ObjectDoesNotExists
from core.permissions import get_user_principles, Permission, DEFAULT_ACL
from repository.calorie import CalorieRepository
from schemas.calorie import Calorie, CalorieList, CalorieCreate
from utils.calorie_calculator import CalorieCalculator

router = APIRouter(prefix='/calorie', tags=['Calorie'])


@router.get(
    path='/user/{user_id}',
    response_model=CalorieList,
    description='Method returns calories list for user'
)
async def get_user_calorie_records(
        user_id: int,
        start_date: Optional[date] = date(1970, 1, 1),
        end_date: Optional[date] = date.today(),
        repository: CalorieRepository = Depends(get_calorie_repository),
        principles: List = Depends(get_user_principles),
):
    calories = await repository.get_all_by_user_id(user_id, start_date, end_date)
    if not all(has_permission(principles, 'view', i) for i in calories):
        raise permission_exception

    used_calories, left_calories = CalorieCalculator(calories).get_statistics()
    return {
        'calories': calories,
        'used': used_calories,
        'left': left_calories
    }


@router.get(
    path='/{calorie_id}',
    response_model=Calorie,
    description='Method returns calorie by id'
)
async def get_calorie_record_by_id(
        calorie_id: int,
        repository: CalorieRepository = Depends(get_calorie_repository),
        principles: List = Depends(get_user_principles)
):
    try:
        calorie = repository.get_by_id(calorie_id)
    except ObjectDoesNotExists as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=e.message)
    if not has_permission(principles, 'view', calorie):
        raise permission_exception

    return calorie


@router.post(
    path='/{user_id}',
    response_model=Calorie,
    description='Method creates calorie record and returns it'
)
async def create_calorie_record(
        user_id: int,
        data: CalorieCreate,
        acls: List = Permission('create', DEFAULT_ACL),
        repository: CalorieRepository = Depends(get_calorie_repository)
):
    try:
        return await repository.create_calorie(user_id, data)
    except ObjectDoesNotExists as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, e.message)


@router.put(
    path='/{calorie_id}',
    response_model=Calorie,
    description='Method updates calorie record and returns it'
)
async def edit_calorie_record(
        calorie_id: int,
        data: CalorieCreate,
        repository: CalorieRepository = Depends(get_calorie_repository),
        principles: List = Depends(get_user_principles)
):
    try:
        calorie = await repository.get_by_id(calorie_id)
    except ObjectDoesNotExists as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, e.message)
    if not has_permission(principles, 'edit', calorie):
        raise permission_exception

    return await repository.update_calorie(calorie, data)


@router.delete(
    path='/{calorie_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    description='Method allows delete calorie record from database'
)
async def delete_calorie_record(
        calorie_id: int,
        repository: CalorieRepository = Depends(get_calorie_repository),
        principles: List = Depends(get_user_principles)
):
    try:
        calorie = await repository.get_by_id(calorie_id)
    except ObjectDoesNotExists:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    if not has_permission(principles, 'delete', calorie):
        raise permission_exception

    await repository.delete_calorie(calorie)
