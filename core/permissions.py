from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi_permissions import Allow, Authenticated, configure_permissions

from core.exceptions import InvalidTokenError
from models.user import User
from utils.user_auth import get_by_token

oauth2_scheme = OAuth2PasswordBearer('users/token')

ADMIN_ACL = [
        (Allow, 'admin:True', 'create'),
        (Allow, 'admin:True', 'view'),
        (Allow, 'admin:True', 'edit'),
        (Allow, 'admin:True', 'delete')
]
DEFAULT_ACL = [
    (Allow, Authenticated, 'batch'),
    (Allow, Authenticated, 'create'),
    (Allow, Authenticated, 'view'),
    (Allow, Authenticated, 'edit'),
    (Allow, Authenticated, 'delete')
]


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        return get_by_token(token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message
        )


def get_user_principals(user: User = Depends(get_current_user)):
    return user.principals + [Authenticated]


Permission = configure_permissions(get_user_principals)
