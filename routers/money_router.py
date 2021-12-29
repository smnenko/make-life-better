from fastapi import APIRouter

from schemas.money_schema import MoneyCreateSchema
from views.money_view import MoneyView

router = APIRouter(prefix='/money', tags=['Money'])


@router.get('/{user_id}')
async def get_all_user_money(user_id: int):
    return MoneyView.get_all_for_user(user_id)


@router.post('/{user_id}')
async def create_money(user_id: int, money: MoneyCreateSchema):
    return MoneyView.create(user_id, money)
