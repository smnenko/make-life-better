from typing import Optional, List
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


class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    birth_date: Optional[date]

    class Config:
        orm_mode = True


class UsersList(BaseModel):
    users: List[User]


class UserCreate(BaseUserCreationSchema, BaseUserValidationSchema):
    pass


class UserUpdate(BaseUserValidationSchema):
    first_name: str
    last_name: str
    birth_date: date
