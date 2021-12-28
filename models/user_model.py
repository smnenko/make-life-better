import bcrypt
from fastapi_permissions import Allow
from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String
from sqlalchemy.sql import func, expression

from models import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(16), unique=True)
    email = Column(String(64), unique=True)
    password = Column(String(256))
    first_name = Column(String(32), nullable=True)
    last_name = Column(String(32), nullable=True)
    birth_date = Column(Date, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())
    is_active = Column(Boolean, nullable=False, server_default=expression.true())
    is_admin = Column(Boolean, nullable=False, server_default=expression.false())

    @property
    def principals(self):
        return [f'user:{self.id}', f'admin:{self.is_admin}']

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def set_password(self, password):
        self.password = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

    def __acl__(self):
        return [
            (Allow, f'user:{self.id}', 'view'),
            (Allow, f'user:{self.id}', 'edit'),
            (Allow, f'user:{self.id}', 'delete'),
            (Allow, 'admin:True', 'edit'),
            (Allow, 'admin:True', 'delete')
        ]

    def __repr__(self):
        return f'<{self.__class__.__name__}>({self.email}, {self.username})'
