from enum import Enum as EnumClass

from sqlalchemy import Column, String, ForeignKey, Integer, Text, Date, Enum
from sqlalchemy.sql import func

from core.database import Base
from models.user import User


class Unit(EnumClass):
    gram = 1
    portion = 2


class Dish(Base):
    __tablename__ = 'dishes'
    id = Column(Integer, primary_key=True, unique=True, index=True)
    title = Column(String(length=256), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    calorie_count = Column(Integer)


class CalorieRecord(Base):
    __tablename__ = 'calories'
    dish_id = Column(ForeignKey(Dish.id), nullable=False)
    user_id = Column(ForeignKey(User.id), nullable=False)
    amount = Column(Integer, nullable=False)
    unit = Column(Enum(Unit), nullable=False)
    date = Column(Date, server_default=func.now(), nullable=False)
