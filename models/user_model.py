import bcrypt
from sqlalchemy import Column, Date, DateTime, Integer, String
from sqlalchemy.sql import func

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

    def __repr__(self):
        return f'<{self.__class__.__name__}>({self.email}, {self.username})'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def set_password(self, password):
        self.password = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')
