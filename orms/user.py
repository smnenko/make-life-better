import re
from datetime import datetime

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from exceptions.user import (
    UserUniqueConstraintException,
    UserDoesNotExists
)
from core.database import engine
from models.user import User
from schemas.user import UserUpdate

Session = sessionmaker()
Session.configure(bind=engine)


class UserOrm:
    session = Session()

    @classmethod
    def _get_field_from_error_msg(cls, msg):
        return re.search(r'(?<=.\()(.*)(?=\)=)', msg).group()

    @classmethod
    def get_all_users(cls):
        return cls.session.query(User).order_by(User.id.asc())

    @classmethod
    def get_by_username(cls, username: str):
        return (
            cls.session
            .query(User)
            .filter(User.username == username)
        ).first()

    @classmethod
    def get_by_id(cls, user_id: int):
        return (
            cls.session
            .query(User)
            .filter(User.id == user_id)
        ).first()

    @classmethod
    def create_user(cls, email, username, password):
        usr = User(username=username, email=email)
        usr.set_password(password)
        try:
            cls.session.add(usr)
            cls.session.commit()
            cls.session.refresh(usr)
            return usr
        except sqlalchemy.exc.IntegrityError as e:
            cls.session.rollback()
            field = f'{cls._get_field_from_error_msg(e.orig.args[0])}'
            detail = f'User with this already {field} exists'
            raise UserUniqueConstraintException(field, detail)

    @classmethod
    def update_user(cls, user: User, data: UserUpdate):
        user.username = data.username
        user.email = data.email
        user.first_name = data.first_name
        user.last_name = data.last_name
        user.birth_date = data.birth_date
        user.updated_at = datetime.now()

        try:
            cls.session.add(user)
            cls.session.commit()
            cls.session.refresh(
                user, [
                    'id',
                    'username',
                    'email',
                    'first_name',
                    'last_name',
                    'birth_date',
                    'updated_at'
                ]
            )
            return user
        except sqlalchemy.exc.IntegrityError as e:
            cls.session.rollback()
            field = cls._get_field_from_error_msg(e.orig.args[0])
            detail = f'User with this already {field} exists'
            raise UserUniqueConstraintException(field, detail)

    @classmethod
    def delete_user(cls, user: User):
        user = cls.session.query(User).filter(User.id == user.id)
        if not isinstance(user.first(), User):
            raise UserDoesNotExists('User with this id doesn\'t exists')

        user.delete()
        cls.session.commit()
