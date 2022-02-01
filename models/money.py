from enum import IntEnum

from fastapi_permissions import Allow
from sqlalchemy import (
    DECIMAL,
    Boolean,
    Column,
    Date,
    Enum,
    ForeignKey,
    Integer, 
    String
)
from sqlalchemy.sql import func

from core.database import Base
from models.user import User


class MoneyType(IntEnum):
    income = 1
    outlay = 2


class MoneyRecord(Base):
    __tablename__ = 'money'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
    type = Column(Enum(MoneyType), nullable=False)
    is_regular = Column(Boolean, nullable=False)
    title = Column(String(length=256), nullable=False)
    amount = Column(DECIMAL(6, 2), nullable=False)
    date = Column(Date, server_default=func.now(), nullable=False)

    def __acl__(self):
        return [
            (Allow, f'user:{self.user_id}', 'view'),
            (Allow, f'user:{self.user_id}', 'edit'),
            (Allow, f'user:{self.user_id}', 'delete'),
            (Allow, 'admin:True', 'view'),
            (Allow, 'admin:True', 'edit'),
            (Allow, 'admin:True', 'delete')
        ]
