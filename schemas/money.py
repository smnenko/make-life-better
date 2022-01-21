from decimal import Decimal
from typing import List

from pydantic import BaseModel

from models.money import MoneyType


class Money(BaseModel):
    id: int
    title: str
    amount: Decimal
    type: MoneyType
    is_regular: bool

    class Config:
        orm_mode = True


class MoneyList(BaseModel):
    monies: List[Money]
    total_incomes: Decimal = None
    total_outlays: Decimal = None


class MoneyCreate(BaseModel):
    title: str
    amount: Decimal
    type: MoneyType
    is_regular: bool
