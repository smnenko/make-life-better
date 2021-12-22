import enum
from datetime import date

from sqlalchemy import DECIMAL, Column, Date, Enum, ForeignKey, Integer, String
from sqlalchemy.sql import func

from models import Base
from models.user_model import User


class MoneyType(enum.Enum):
    income = 1
    outlay = 2


class Money(Base):
    __tablename__ = 'money'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
    type = Column(Enum(MoneyType), nullable=False)
    amount = Column(DECIMAL(2), nullable=False)
    date = Column(Date, server_default=func.now(), nullable=False)
