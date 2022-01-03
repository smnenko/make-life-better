from fastapi import APIRouter

from schemas.money import MoneyCreateSchema
from views.money import MoneyView

router = APIRouter(prefix='/money', tags=['Money'])


@router.get('/{money_id}')
async def get_money(money_id: int):
    return MoneyView.get(money_id)


@router.get('/{user_id}/day')
async def get_today_user_money(user_id: int):
    return MoneyView.get_today_for_user(user_id)


@router.get('/{user_id}/week')
async def get_week_user_money(user_id: int):
    return MoneyView.get_week_for_user(user_id)


@router.get('/{user_id}/month')
async def get_month_user_money(user_id: int):
    return MoneyView.get_month_for_user(user_id)


@router.get('/{user_id}/all')
async def get_all_user_money(user_id: int):
    return MoneyView.get_all_for_user(user_id)


@router.post('/{user_id}')
async def create_money(user_id: int, money: MoneyCreateSchema):
    return MoneyView.create(user_id, money)


@router.put('/{money_id}')
async def edit_money(money_id: int, data: MoneyCreateSchema):
    return MoneyView.update(money_id, data)


@router.delete('/{money_id}')
async def delete_money(money_id: int):
    return MoneyView.delete(money_id)
