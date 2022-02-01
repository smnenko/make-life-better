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
    def _get_field_from_error_msg(cls, msg):
        return re.search(r'(?<=.\()(.*)(?=\)=)', msg).group()

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
        usr = User(username=data.username, email=data.email)
        usr.set_password(data.password)
        try:
            self.session.add(usr)
            await self.session.commit()
            await self.session.refresh(usr, [
                    'id',
                    'username',
                    'email',
                    'first_name',
                    'last_name',
                    'birth_date'
                ])
            return usr
        except sqlalchemy.exc.IntegrityError as e:
            await self.session.rollback()
            field = self._get_field_from_error_msg(msg=str(e))
            detail = f'User with this {field} already exists'
            raise ObjectAlreadyExistsError(field, detail)

    async def update_user(self, user: User, data: UserUpdate):
        user.username = data.username
        user.email = data.email
        user.first_name = data.first_name
        user.last_name = data.last_name
        user.birth_date = data.birth_date
        user.updated_at = datetime.now()

        try:
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
        except sqlalchemy.exc.IntegrityError as e:
            await self.session.rollback()
            field = self._get_field_from_error_msg(e)
            detail = f'User with this already {field} exists'
            raise ObjectAlreadyExistsError(field, detail)

    async def delete_user(self, user: User):
        await self.session.delete(user)
        await self.session.commit()
