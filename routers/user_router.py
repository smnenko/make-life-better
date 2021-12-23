from fastapi import APIRouter
from fastapi_utils.cbv import cbv, Depends

from schemas.user_schema import UserCreateSchema, UserUpdateSchema
from views.user_view import UserView

router = APIRouter(prefix='/users', tags=['Users'])


@cbv(router)
class UserRouter:

    @router.get('/')
    async def get_all_users(self):
        return UserView.get_all()

    @router.get('/{user_id}')
    async def get_user(self, user_id: int):
        return UserView.get(user_id)

    @router.post('/')
    async def create_user(self, user: UserCreateSchema):
        return UserView.create(user)

    @router.put('/')
    async def update_user(self, user: UserUpdateSchema):
        return UserView.update(user)

    @router.delete('/{user_id}')
    async def delete_user(self, user_id: int):
        return UserView.delete(user_id)
