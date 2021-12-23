from fastapi import APIRouter
from fastapi_utils.cbv import cbv


router = APIRouter(prefix='/money', tags=['Money'])


@cbv(router)
class MoneyRouter:

    @router.get('/{user_id}')
    async def get_user_money(self, user_id: int):
        return

    @router.post('/{user_id}')
    async def create_money(self, user_id: int):
        return
