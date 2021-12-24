from fastapi import HTTPException, status

from exceptions.user_exceptions import InvalidCredentialsException
from utils.user_util import UserUtil


def authenticated_permission(func):
    def wrapper(*args, **kwargs):
        try:
            _, user_id, request = args
            token = request.headers.get('Authorization')
            if token:
                user = UserUtil.get_current_user(token)
                if user:
                    func(user_id)
            else:
                raise InvalidCredentialsException('Invalid credentials')
        except InvalidCredentialsException as e:
            return HTTPException(status.HTTP_401_UNAUTHORIZED, e)
    return wrapper
