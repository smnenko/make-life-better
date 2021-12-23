from decimal import Decimal

from pydantic import BaseModel


class MoneyRetrieveSchema(BaseModel):
    title: str
    amount: Decimal
    type: int
