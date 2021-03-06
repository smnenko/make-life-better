import os
from datetime import datetime, timedelta

import bcrypt
from jose import JWTError, jwt

from core.database import async_session
from core.exceptions import InvalidTokenError
from repository.user import UserRepository

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


async def get_by_token(token: str):
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

    async with async_session() as session:
        user = await UserRepository(session).get_by_username(username)
        if user is None or not user.is_active:
            raise credentials_exception

        return user


def verify_password(hashed_password: str, password: str):
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )


async def authenticate(username: str, password: str):
    async with async_session() as session:
        user = await UserRepository(session).get_by_username(username)

        if not user:
            return False
        if not verify_password(user.password, password):
            return False

        return user


def create_access_token(
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
