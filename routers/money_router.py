from fastapi import APIRouter, Request
from fastapi_utils.cbv import cbv

from views.money_view import MoneyView

router = APIRouter(prefix='/money', tags=['Money'])


@router.get('/{user_id}')
async def get_all_user_money(user_id: int, request: Request):
    return MoneyView.get_all_for_user(user_id, request)


@router.post('/{user_id}')
async def create_money(user_id: int):
    return
