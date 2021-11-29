import re
from datetime import datetime

import sqlalchemy.exc
from sqlalchemy.orm import sessionmaker

from models import engine
from models.user import User
from schemas.user import UserRetrieveSchema


Session = sessionmaker()
Session.configure(bind=engine)


class UserUtil:

    session = Session()

    @classmethod
    def _get_by_username(cls, username):
        return UserRetrieveSchema.parse_obj(
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
            field = cls.get_field_from_error_msg(e.orig.args[0])
            return {'details': f'This {field} already taken'}
        return usr

    @classmethod
    def get_all(cls):
        return [
            UserRetrieveSchema.parse_obj(i.__dict__)
            for i in cls.session.query(User).all()
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
        try:
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
            cls.session.add(usr)
            cls.session.commit()
            cls.session.refresh(usr, [
                'id', 'username', 'email', 'first_name', 'last_name', 'birth_date', 'updated_at'
            ])

        except sqlalchemy.exc.IntegrityError as e:
            cls.session.rollback()
            field = cls.get_field_from_error_msg(e.orig.args[0])
            return {'details': f'This {field} already taken'}
        return UserRetrieveSchema.parse_obj(usr.__dict__)

    @classmethod
    def delete_by_id(cls, user_id):
        cls._get_by_id(user_id).delete()
        cls.session.commit()
        return {'details': 'Deleted'}
