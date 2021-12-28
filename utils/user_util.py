import os
import re
from datetime import datetime, timedelta

import bcrypt
import sqlalchemy
from jose import jwt, JWTError
from sqlalchemy.orm import sessionmaker

from exceptions.user_exceptions import (
    UserUniqueConstraintException,
    UserDoesNotExists,
    InvalidTokenError
)
from models import engine
from models.user_model import User


SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


Session = sessionmaker()
Session.configure(bind=engine)


class UserUtil:
    session = Session()

    @classmethod
    def get_field_from_error_msg(cls, msg):
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
    def get_by_token(cls, token: str):
        credentials_exception = InvalidTokenError(
            'Could not validate credentials'
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get('username')
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        user = cls.get_by_username(username)
        if user is None:
            raise credentials_exception
        return user

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
            field = f'{cls.get_field_from_error_msg(e.orig.args[0])}'
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
            field = cls.get_field_from_error_msg(e.orig.args[0])
            detail = f'User with this already {field} exists'
            raise UserUniqueConstraintException(field, detail)

    @classmethod
    def delete_user(cls, user_id: int):
        user = cls.session.query(User).filter(User.id == user_id)
        if not isinstance(user.first(), User):
            raise UserDoesNotExists('User with this id doesn\'t exists')

        user.delete()
        cls.session.commit()

    @classmethod
    def verify_password(cls, hashed_password: str, password: str):
        return bcrypt.checkpw(
            password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )

    @classmethod
    def authenticate(cls, username: str, password: str):
        user = cls.get_by_username(username)
        if not user:
            return False
        if not cls.verify_password(user.password, password):
            return False

        return user

    @classmethod
    def create_access_token(
            cls,
            data: dict,
            expired_min=ACCESS_TOKEN_EXPIRE_MINUTES
    ):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=expired_min)
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(
            to_encode,
            SECRET_KEY.encode('utf-8'),
            algorithm=ALGORITHM
        )
        return encoded_jwt
