from datetime import date
from typing import List

from pydantic import BaseModel

from models.calorie import Unit


class Dish(BaseModel):
    id: int
    title: str
    calorie_count: int

    class Config:
        orm_mode = True


class DishList(BaseModel):
    dishes: List[Dish]
    total: int


class Calorie(BaseModel):
    id: int
    dish: Dish
    amount: int
    unit: Unit
    calories: float
    date: date

    class Config:
        orm_mode = True


class CalorieCreate(BaseModel):
    dish_id: int
    amount: int
    unit: Unit


class CalorieList(BaseModel):
    calories: List[Calorie]
    used: float
    left: float
