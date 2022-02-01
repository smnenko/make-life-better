from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi_permissions import has_permission, permission_exception

from core.exceptions import ObjectDoesNotExists
from core.permissions import DEFAULT_ACL, Permission, get_user_principles
from models.money import MoneyRecord
from repository.money import MoneyRepository
from schemas.money import Money, MoneyCreate, MoneyList
from utils.money_calculator import MoneyTotalsCalculator

router = APIRouter(prefix='/money', tags=['Money'])


@router.get('/{money_id}')
async def get_money_record(
        money_id: int,
        money: Optional[MoneyRecord] = Permission('view', MoneyRepository.get_by_id)
):
    if not money:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            'Money record not found'
        )
    return MoneyRecord.from_orm(money)


@router.get('/user/{user_id}')
async def get_all_user_money_records(
        user_id: int,
        start_date: date,
        end_date: date,
        monies: List[MoneyRecord] = Depends(MoneyRepository.get_all_by_user_id),
        principals: List = Depends(get_user_principles),
        acls: List = Permission('batch', DEFAULT_ACL)
):
    if not all(has_permission(principals, 'view', i) for i in monies):
        raise permission_exception

    incomes, outlays = MoneyTotalsCalculator(monies).get_tuple_result()
    return MoneyList(
        monies=[Money.from_orm(i) for i in monies],
        total_incomes=incomes,
        total_outlays=outlays
    )


@router.post('/{user_id}')
async def create_money_record(
        user_id: int,
        data: MoneyCreate,
        acls: List = Permission('create', DEFAULT_ACL)
):
    money = MoneyRepository.create_money(user_id, data)
    return Money.from_orm(money)


@router.put('/{money_id}')
async def edit_money_record(
        money_id: int,
        data: MoneyCreate,
        money: Optional[MoneyRecord] = Depends(MoneyRepository.get_by_id),
        principles: List = Depends(get_user_principles),
        acls: List = Permission('edit', DEFAULT_ACL)
):
    if not has_permission(principles, 'delete', money):
        raise permission_exception

    try:
        money = MoneyRepository.update_money(money, data)
        return Money.from_orm(money)
    except ObjectDoesNotExists as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, e.message)


@router.delete('/{money_id}')
async def delete_money_record(
        money_id: int,
        money: Optional[MoneyRecord] = Depends(MoneyRepository.get_by_id),
        principles: List = Depends(get_user_principles),
        acls: List = Permission('delete', DEFAULT_ACL)
):
    if not has_permission(principles, 'delete', money):
        raise permission_exception

    try:
        MoneyRepository.delete_money(money)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExists:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
