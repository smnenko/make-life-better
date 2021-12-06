import os
import re
from datetime import datetime, timedelta

import bcrypt
from fastapi import status, HTTPException, Response
import sqlalchemy.exc
from jose import jwt, JWTError
from sqlalchemy.orm import sessionmaker

from models import engine
from models.user_model import User
from schemas.user_schema import UserRetrieveSchema


SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


Session = sessionmaker()
Session.configure(bind=engine)


def verify_password(hashed_password, password):
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )


def authenticate(username, password):
    user = UserUtil()._get_by_username(username).first()
    if not user:
        return False
    if not verify_password(user.password, password):
        return False

    return user


def create_access_token(data: dict, expired_min=ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expired_min)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY.encode('utf-8'), algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str):
    credentials_exception = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        'Could not validate credentials'
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = UserUtil._get_by_username(username)
    if user.first() is None:
        raise credentials_exception
    return user


class UserUtil:

    session = Session()

    @classmethod
    def _get_by_username(cls, username):
        return (
            cls.session
            .query(User)
            .filter(User.username == username)
        )

    @classmethod
    def _get_by_id(cls, user_id):
        return (
            cls.session
            .query(User)
            .filter(User.id == user_id)
        )

    @classmethod
    def get_field_from_error_msg(cls, msg):
        return re.search(r'(?<=.\()(.*)(?=\)=)', msg).group()

    @classmethod
    def create_user(cls, user):
        usr = User(username=user.username, email=user.email)
        usr.set_password(user.password)
        try:
            cls.session.add(usr)
            cls.session.commit()
            cls.session.refresh(usr)
        except sqlalchemy.exc.IntegrityError as e:
            cls.session.rollback()
            field = f'{cls.get_field_from_error_msg(e.orig.args[0])}'
            detail = f'User with this already {field} exists'
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail)
        return usr

    @classmethod
    def get_all(cls):
        return [
            UserRetrieveSchema.parse_obj(i.__dict__)
            for i in cls.session.query(User).order_by(User.id.asc())
        ]

    @classmethod
    def get_by_id(cls, user_id):
        user = cls._get_by_id(user_id).first()
        return UserRetrieveSchema.parse_obj(
            user.__dict__
        ) if user else None

    @classmethod
    def update_user(cls, user):
        usr: User = cls._get_by_id(user.id).first()
        if not usr:
            new_user = User(**user.__dict__)
            new_user.id = None
            cls.session.add(new_user)
            cls.session.commit()
            cls.session.refresh(new_user)
            return UserRetrieveSchema.parse_obj(new_user.__dict__)

        usr.username = user.username
        usr.email = user.email
        usr.first_name = user.first_name
        usr.last_name = user.last_name
        usr.birth_date = user.birth_date
        usr.updated_at = datetime.now()

        try:
            cls.session.add(usr)
            cls.session.commit()
            cls.session.refresh(usr, [
                'id', 'username', 'email', 'first_name', 'last_name', 'birth_date', 'updated_at'
            ])

        except sqlalchemy.exc.IntegrityError as e:
            cls.session.rollback()
            field = cls.get_field_from_error_msg(e.orig.args[0])
            detail = f'This {field} already taken'
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail)
        return UserRetrieveSchema.parse_obj(usr.__dict__)

    @classmethod
    def delete_by_id(cls, user_id):
        user = cls._get_by_id(user_id)
        if not isinstance(user.first(), User):
            raise HTTPException(status.HTTP_204_NO_CONTENT)

        user.delete()
        cls.session.commit()
        return Response(status_code=status.HTTP_200_OK)

    @classmethod
    def token(cls, username, password):
        user = authenticate(username, password)
        if not user:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                'Username or password is invalid'
            )

        access_token = create_access_token({'username': username})
        return {'access_token': access_token, 'token_type': 'Bearer'}
