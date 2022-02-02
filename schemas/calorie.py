from datetime import date
from typing import List, Optional

from pydantic import BaseModel


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
    date: date

    class Config:
        orm_mode = True


class CalorieCreate(BaseModel):
    dish_id: int
    date: date
    amount: int


class CalorieList(BaseModel):
    calories: List[Calorie]
    used: Optional[float]
    left: Optional[float]
