import re
from datetime import datetime

import sqlalchemy
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.exceptions import ObjectDoesNotExists, ObjectAlreadyExistsError
from models.user import User
from schemas.user import UserUpdate, UserCreate


class UserRepository:

    def __init__(self, session: Session):
        self.session = session

    @classmethod
    def _get_field_from_error_msg(cls, msg: str):
        return re.search(r'(?<=.\()(.*)(?=\)=)', msg).group()

    def _get_unique_violation_exception(self, e: Exception):
        field = self._get_field_from_error_msg(msg=str(e))
        detail = f'User with this {field} already exists'
        return ObjectAlreadyExistsError(field, detail)

    async def _create_user(self, data: UserCreate):
        user = User(username=data.username, email=data.email)
        user.set_password(data.password)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user, [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'birth_date'
        ])
        return user

    async def _update_user(self, user: User, data: UserUpdate):
        user.username = data.username
        user.email = data.email
        user.first_name = data.first_name
        user.last_name = data.last_name
        user.birth_date = data.birth_date
        user.updated_at = datetime.now()

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(
            user, [
                'id',
                'username',
                'email',
                'first_name',
                'last_name',
                'birth_date'
            ]
        )
        return user

    async def get_all_users(self):
        query = select(User).order_by(User.id.asc())
        return (await self.session.execute(query)).scalars().all()

    async def get_by_username(self, username: str):
        query = select(User).where(User.username == username)
        return (await self.session.execute(query)).scalars().one()

    async def get_by_id(self, user_id: int):
        query = select(User).where(User.id == user_id)
        try:
            return (await self.session.execute(query)).scalars().one()
        except sqlalchemy.exc.NoResultFound:
            raise ObjectDoesNotExists('User doesn\'t exists')

    async def create_user(self, data: UserCreate):
        try:
            return await self._create_user(data)
        except sqlalchemy.exc.IntegrityError as e:
            await self.session.rollback()
            raise self._get_unique_violation_exception(e)

    async def update_user(self, user: User, data: UserUpdate):
        try:
            return await self._update_user(user, data)
        except sqlalchemy.exc.IntegrityError as e:
            await self.session.rollback()
            raise self._get_unique_violation_exception(e)

    async def delete_user(self, user: User):
        await self.session.delete(user)
        await self.session.commit()
