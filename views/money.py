from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi_permissions import has_permission, permission_exception

from core.permissions import MONEY_ACL, Permission, get_user_principals
from exceptions.money import MoneyRecordDoesNotExist
from models.money import Money as MoneyDB
from orms.money import MoneyOrm
from schemas.money import Money, MoneyCreate, MoneyList
from utils.money_calculator import MoneyTotalsCalculator

router = APIRouter(prefix='/money', tags=['Money'])


@router.get('/{money_id}')
async def get_money_record(
        money_id: int,
        money: Money = Permission('view', MoneyOrm.get_by_id)
):
    if not money:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            'Money record not found'
        )
    return Money.from_orm(money)


@router.get('/{user_id}/day')
async def get_today_user_money_records(
        user_id: int,
        monies: List[MoneyDB] = Depends(MoneyOrm.get_today_by_user_id),
        principals: list = Depends(get_user_principals),
        acls: list = Permission('batch', MONEY_ACL)
):
    if not all(has_permission(principals, 'view', i) for i in monies):
        raise permission_exception

    incomes, outlays = MoneyTotalsCalculator(monies).get_tuple_result()
    return MoneyList(
        monies=[Money.from_orm(i) for i in monies],
        total_incomes=incomes,
        total_outlays=outlays
    )


@router.get('/{user_id}/week')
async def get_week_user_money_records(
        user_id: int,
        monies: List[MoneyDB] = Depends(MoneyOrm.get_week_by_user_id),
        principals: list = Depends(get_user_principals),
        acls: list = Permission('batch', MONEY_ACL)
):
    if not all(has_permission(principals, 'view', i) for i in monies):
        raise permission_exception

    incomes, outlays = MoneyTotalsCalculator(monies).get_tuple_result()
    return MoneyList(
        monies=[Money.from_orm(i) for i in monies],
        total_incomes=incomes,
        total_outlays=outlays
    )


@router.get('/{user_id}/month')
async def get_month_user_money_records(
        user_id: int,
        monies: List[MoneyDB] = Depends(MoneyOrm.get_month_by_user_id),
        principals: list = Depends(get_user_principals),
        acls: list = Permission('batch', MONEY_ACL)
):
    if not all(has_permission(principals, 'view', i) for i in monies):
        raise permission_exception

    incomes, outlays = MoneyTotalsCalculator(monies).get_tuple_result()
    return MoneyList(
        monies=[Money.from_orm(i) for i in monies],
        total_incomes=incomes,
        total_outlays=outlays
    )


@router.get('/{user_id}/all')
async def get_all_user_money_records(
        user_id: int,
        monies: List[MoneyDB] = Depends(MoneyOrm.get_all_by_user_id),
        principals: list = Depends(get_user_principals),
        acls: list = Permission('batch', MONEY_ACL)
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
        acls: list = Permission('create', MONEY_ACL)
):
    money = MoneyOrm.create_money(user_id, data)
    return Money.from_orm(money)


@router.put('/{money_id}')
async def edit_money_record(
        money_id: int,
        data: MoneyCreate,
        money: MoneyDB = Depends(MoneyOrm.get_by_id),
        principles: list = Depends(get_user_principals),
        acls: list = Permission('edit', MONEY_ACL)
):
    if not has_permission(principles, 'delete', money):
        raise permission_exception

    try:
        money = MoneyOrm.update_money(money, data)
        return Money.from_orm(money)
    except MoneyRecordDoesNotExist as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, e.message)


@router.delete('/{money_id}')
async def delete_money_record(
        money_id: int,
        money: MoneyDB = Depends(MoneyOrm.get_by_id),
        principles: list = Depends(get_user_principals),
        acls: list = Permission('delete', MONEY_ACL)
):
    if not has_permission(principles, 'delete', money):
        raise permission_exception

    try:
        MoneyOrm.delete_money(money)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except MoneyRecordDoesNotExist:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
