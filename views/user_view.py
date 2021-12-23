from fastapi import HTTPException, status

from exceptions.user_exceptions import UserUniqueConstraintException, UserDoesNotExists
from schemas.user_schema import UserRetrieveSchema, UserCreateSchema, UserUpdateSchema
from utils.user_util import UserUtil


class UserView:

    @classmethod
    def get_all(cls):
        return [
            UserRetrieveSchema.parse_obj(i.__dict__)
            for i in UserUtil.get_all_users()
        ]

    @classmethod
    def get(cls, user_id: int):
        user = UserUtil.get_by_id(user_id).first()
        if user:
            return UserRetrieveSchema.parse_obj(user.__dict__)
        return HTTPException(status.HTTP_204_NO_CONTENT)

    @classmethod
    def create(cls, user: UserCreateSchema):
        try:
            user = UserUtil.create_user(
                email=user.email,
                username=user.username,
                password=user.password
            )
            return UserRetrieveSchema.parse_obj(user.__dict__)
        except UserUniqueConstraintException as e:
            return HTTPException(status.HTTP_400_BAD_REQUEST, detail=e.message)

    @classmethod
    def update(cls, user: UserUpdateSchema):
        try:
            user = UserUtil.update_user(
                id_=user.id,
                email=user.email,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                birth_date=user.birth_date,
                password=user.password
            )
            return UserRetrieveSchema.parse_obj(usr.__dict__)
        except UserUniqueConstraintException as e:
            return HTTPException(status.HTTP_400_BAD_REQUEST, detail=e.message)

    @classmethod
    def delete(cls, user_id: int):
        try:
            UserUtil.delete_user(user_id)
            return {'status': 'Deleted'}
        except UserDoesNotExists as e:
            return HTTPException(status.HTTP_204_NO_CONTENT, detail=e.message)

    @classmethod
    def token(cls, username, password):
        user = UserUtil.authenticate(username, password)
        if not user:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                'Username or password is invalid'
            )

        access_token = UserUtil.create_access_token({'username': username})
        return {'access_token': access_token, 'token_type': 'Bearer'}
