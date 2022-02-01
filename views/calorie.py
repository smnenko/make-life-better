from datetime import date
from typing import List, Optional

from fastapi import Depends, HTTPException, status, Response
from fastapi.routing import APIRouter
from fastapi_permissions import has_permission, permission_exception

from core.exceptions import ObjectDoesNotExists
from core.permissions import get_user_principles, Permission, DEFAULT_ACL
from repository.calorie import CalorieRepository
from models.calorie import CalorieRecord
from schemas.calorie import Calorie, CalorieList, CalorieCreate
from utils.calorie_calculator import CalorieCalculator

router = APIRouter(prefix='/calorie', tags=['Calorie'])


@router.get('/user/{user_id}')
async def get_user_calorie_records(
        user_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        calories: List[CalorieRecord] = Depends(CalorieRepository.get_all_by_user_id),
        principles: List = Depends(get_user_principles),
        acls: List = Permission('batch', DEFAULT_ACL)
):
    if not all(has_permission(principles, 'view', i) for i in calories):
        raise permission_exception

    used_calories, left_calories = CalorieCalculator(calories).get_statistics()
    return CalorieList(
        calories=[Calorie.from_orm(i) for i in calories],
        used=used_calories,
        left=left_calories
    )


@router.get('/{calorie_id}')
async def get_calorie_record_by_id(
        calorie_id: int,
        calorie: Optional[CalorieRecord] = Permission('view', CalorieRepository.get_by_id)
):
    if not calorie:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            'Calorie record not found'
        )
    return Calorie.from_orm(calorie)


@router.post('/{user_id}')
async def create_calorie_record(
        user_id: int,
        data: CalorieCreate,
        acls: List = Permission('create', DEFAULT_ACL)
):
    try:
        calorie = CalorieRepository.create_calorie(user_id, data)
        return Calorie.from_orm(calorie)
    except ObjectDoesNotExists as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, e.message)


@router.put('/{calorie_id}')
async def edit_calorie_record(
        calorie_id: int,
        data: CalorieCreate,
        calorie: Optional[CalorieRecord] = Permission('edit', CalorieRepository.get_by_id)
):
    calorie = CalorieRepository.update_calorie(calorie, data)
    return Calorie.from_orm(calorie)


@router.delete('/{calorie_id}')
async def delete_calorie_record(
        calorie_id: int,
        calorie: Optional[CalorieRecord] = Permission('delete', CalorieRepository.get_by_id)
):
    if not calorie:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    CalorieRepository.delete_calorie(calorie)
    return Response(status.HTTP_204_NO_CONTENT)
