from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi_permissions import has_permission, permission_exception

from core.dependencies import get_money_repository
from core.exceptions import ObjectDoesNotExists
from core.permissions import DEFAULT_ACL, Permission, get_user_principles
from repository.money import MoneyRepository
from schemas.money import Money, MoneyCreate, MoneyList
from utils.money_calculator import MoneyTotalsCalculator

router = APIRouter(prefix='/money', tags=['Money'])


@router.get(
    path='/user/{user_id}',
    response_model=MoneyList,
    description='Method return list of monies with calculated incomes and outlays'
)
async def get_all_user_money_records(
        user_id: int,
        start_date: Optional[date] = date(1970, 1, 1),
        end_date: Optional[date] = date.today(),
        repository: MoneyRepository = Depends(get_money_repository),
        principals: List = Depends(get_user_principles),
):
    monies = await repository.get_all_by_user_id(user_id, start_date, end_date)
    if not all(has_permission(principals, 'view', i) for i in monies):
        raise permission_exception

    incomes, outlays = MoneyTotalsCalculator(monies).get_tuple_result()
    return {
        'monies': monies,
        'total_incomes': incomes,
        'total_outlays': outlays
    }


@router.get(
    path='/{money_id}',
    response_model=Money,
    description='Method returns money record if user has required permissions'
)
async def get_money_record(
        money_id: int,
        repository: MoneyRepository = Depends(get_money_repository),
        principles: List = Depends(get_user_principles)
):
    money = await repository.get_by_id(money_id)
    if has_permission(principles, 'view', money):
        return money
    raise HTTPException(status.HTTP_400_BAD_REQUEST)


@router.post(
    path='/{user_id}',
    response_model=Money,
    description='Method creates new money record and returns it'
)
async def create_money_record(
        user_id: int,
        data: MoneyCreate,
        acls: List = Permission('create', DEFAULT_ACL),
        repository: MoneyRepository = Depends(get_money_repository)
):
    return await repository.create_money(user_id, data)


@router.put(
    path='/{money_id}',
    response_model=Money,
    description='Method allows to update money record model and return it out'
)
async def edit_money_record(
        money_id: int,
        data: MoneyCreate,
        repository: MoneyRepository = Depends(get_money_repository),
        principles: List = Depends(get_user_principles),
):
    try:
        money = await repository.get_by_id(money_id)
    except ObjectDoesNotExists as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, e.message)
    if not has_permission(principles, 'edit', money):
        raise permission_exception

    return await repository.update_money(money, data)


@router.delete(
    path='/{money_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    description='Method allows to delete money record entity from database'
)
async def delete_money_record(
        money_id: int,
        repository: MoneyRepository = Depends(get_money_repository),
        principles: List = Depends(get_user_principles),
):
    try:
        money = await repository.get_by_id(money_id)
    except ObjectDoesNotExists:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    if not has_permission(principles, 'delete', money):
        raise permission_exception

    await repository.delete_money(money)
