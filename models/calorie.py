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
    dish_id = Column(Integer, ForeignKey(Dish.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    amount = Column(Integer, nullable=False)
    date = Column(Date, server_default=func.now(), nullable=False)

    dish = relationship('Dish', backref='dish')
    user = relationship('User', backref='user')
