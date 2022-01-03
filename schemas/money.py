from decimal import Decimal
from typing import List, Optional

from fastapi_permissions import Allow
from pydantic import BaseModel, validator

from models.money import MoneyType


class MoneyRetrieveSchema(BaseModel):
    id: int
    title: str
    amount: Decimal
    type: MoneyType
    is_regular: bool

    class Config:
        orm_mode = True


class MoneyCreateSchema(BaseModel):
    title: str
    amount: Decimal
    type: MoneyType
    is_regular: bool


class MoneyRetrieveAllSchema(BaseModel):
    monies: List[MoneyRetrieveSchema]

    def get_total_incomes(self):
        return sum(
            i.amount
            for i in self.monies
            if i.type == MoneyType.income.value
        )

    def get_total_outlays(self):
        return sum(
            i.amount
            for i in self.monies
            if i.type == MoneyType.outlay.value
        )
