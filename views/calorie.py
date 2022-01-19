from typing import List

from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi_permissions import has_permission, permission_exception

from core.permissions import get_user_principals, Permission, DEFAULT_ACL
from crud.calorie import CalorieOrm
from models.calorie import CalorieRecord
from schemas.calorie import Calorie, CalorieList
from utils.calorie_calculator import CalorieCalculator

router = APIRouter(prefix='/calorie', tags=['Calorie'])


@router.get('/{user_id}/all')
async def get_all_user_calorie_records(
        user_id: int,
        calories: List[CalorieRecord] = Depends(CalorieOrm.get_all_by_user_id),
        principles: List = Depends(get_user_principals),
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
