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
    def update_user(
            cls,
            id_,
            email,
            username,
            first_name,
            last_name,
            birth_date,
    ):
        usr: User = cls.get_by_id(id_)
        usr.username = username
        usr.email = email
        usr.first_name = first_name
        usr.last_name = last_name
        usr.birth_date = birth_date
        usr.updated_at = datetime.now()

        try:
            cls.session.add(usr)
            cls.session.commit()
            cls.session.refresh(
                usr, [
                    'id',
                    'username',
                    'email',
                    'first_name',
                    'last_name',
                    'birth_date',
                    'password',
                    'updated_at'
                ]
            )
            return usr
        except sqlalchemy.exc.IntegrityError as e:
            cls.session.rollback()
            field = cls._get_field_from_error_msg(e.orig.args[0])
            detail = f'User with this already {field} exists'
            raise UserUniqueConstraintException(field, detail)

    @classmethod
    def delete_user(cls, user_id: int):
        user = cls.session.query(User).filter(User.id == user_id)
        if not isinstance(user.first(), User):
            raise UserDoesNotExists('User with this id doesn\'t exists')

        user.delete()
        cls.session.commit()
