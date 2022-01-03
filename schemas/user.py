from typing import Optional
from datetime import date

from pydantic import BaseModel, EmailStr, validator


class BaseUserCreationSchema(BaseModel):
    password: str
    password_confirm: str

    @validator('password_confirm')
    def validate_password(cls, field, values):
        if field != values.get('password'):
            raise ValueError('Passwords don\'t match')
        return field


class BaseUserValidationSchema(BaseModel):
    username: str
    email: EmailStr

    @classmethod
    def is_username_space_valid(cls, username: str):
        if ' ' in username:
            raise ValueError('Username should\t contain a space')
        return True

    @classmethod
    def is_username_alpha_valid(cls, username: str):
        if not username.isalpha():
            raise ValueError(
                'Username should consists of alphabetical characters'
            )
        return True

    @validator('username')
    def validate_username(cls, field):
        if (
                cls.is_username_space_valid(field)
                and cls.is_username_alpha_valid(field)
        ):
            return field


class UserCreateSchema(BaseUserCreationSchema, BaseUserValidationSchema):
    pass


class UserRetrieveSchema(BaseModel):
    id: int
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    birth_date: Optional[date]


class UserUpdateSchema(BaseUserValidationSchema):
    first_name: str
    last_name: str
    birth_date: date