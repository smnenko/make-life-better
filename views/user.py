from fastapi import HTTPException, Response, status

from exceptions.user import UserUniqueConstraintException, UserDoesNotExists
from schemas.user import UserRetrieveSchema, UserCreateSchema, UserUpdateSchema
from orms.user import UserOrm
from utils.user_auth import authenticate, create_access_token


class UserView:

    @classmethod
    def get_all(cls):
        return [
            UserRetrieveSchema.parse_obj(i.__dict__)
            for i in UserOrm.get_all_users()
        ]

    @classmethod
    def get(cls, user_id: int):
        user = UserOrm.get_by_id(user_id)
        if user:
            return UserRetrieveSchema.parse_obj(user.__dict__)
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    @classmethod
    def create(cls, user: UserCreateSchema):
        try:
            user = UserOrm.create_user(
                email=user.email,
                username=user.username,
                password=user.password
            )
            return UserRetrieveSchema.parse_obj(user.__dict__)
        except UserUniqueConstraintException as e:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=e.message)

    @classmethod
    def update(cls, user_id: int, data: UserUpdateSchema):
        try:
            user = UserOrm.update_user(
                id_=user_id,
                email=data.email,
                username=data.username,
                first_name=data.first_name,
                last_name=data.last_name,
                birth_date=data.birth_date,
            )
            return UserRetrieveSchema.parse_obj(user.__dict__)
        except UserUniqueConstraintException as e:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=e.message)

    @classmethod
    def delete(cls, user_id: int):
        try:
            UserOrm.delete_user(user_id)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        except UserDoesNotExists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def token(cls, username: str, password: str):
        user = authenticate(username, password)
        if not user:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                'Username or password is invalid'
            )

        access_token = create_access_token({'username': username})
        return {'access_token': access_token, 'token_type': 'Bearer'}
