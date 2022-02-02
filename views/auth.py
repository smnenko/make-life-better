from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from core.security import authenticate, create_access_token
from schemas.auth import Token


router = APIRouter(tags=['Authentication'])


@router.post(
    path='/token',
    response_model=Token,
    description='Method provides JWT authentication for is_active users'
)
async def get_access_token(credentials: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate(credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            'Username or password is invalid'
        )

    access_token = create_access_token({'username': credentials.username})
    return {'access_token': access_token, 'token_type': 'Bearer'}
