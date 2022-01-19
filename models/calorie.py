from sqlalchemy import Column, String, ForeignKey, Integer, Text, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.database import Base
from models.user import User


class Dish(Base):
    __tablename__ = 'dishes'
    id = Column(Integer, primary_key=True, unique=True, index=True)
    title = Column(String(length=256), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    calorie_count = Column(Integer)


class CalorieRecord(Base):
    __tablename__ = 'calories'
    id = Column(Integer, primary_key=True, unique=True, index=True)
    dish = relationship('Dish', back_populates='dish')
    user = relationship('User', back_populates='user')
    amount = Column(Integer, nullable=False)
    date = Column(Date, server_default=func.now(), nullable=False)
