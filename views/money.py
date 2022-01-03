from datetime import date

from fastapi import HTTPException, status, Response

from exceptions.money import MoneyRecordDoesNotExist
from schemas.money import (
    MoneyCreateSchema,
    MoneyRetrieveAllSchema,
    MoneyRetrieveSchema
)
from orms.money import MoneyOrm
from utils.money_calculator import get_calculated_totals


class MoneyView:

    @classmethod
    def get(cls, money_id: int):
        money = MoneyOrm.get_by_id(money_id)
        if not money:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                'Money record not found'
            )
        return MoneyRetrieveSchema.parse_obj(money.__dict__)

    @classmethod
    def get_today_for_user(cls, user_id: int):
        monies = MoneyOrm.get_today_by_user_id(user_id)
        monies_data = MoneyRetrieveAllSchema(
            monies=[MoneyRetrieveSchema.parse_obj(i.__dict__) for i in monies]
        )
        return get_calculated_totals(monies_data)

    @classmethod
    def get_week_for_user(cls, user_id: int):
        monies = MoneyOrm.get_week_by_user_id(user_id)
        monies_data = MoneyRetrieveAllSchema(
            monies=[MoneyRetrieveSchema.parse_obj(i.__dict__) for i in monies]
        )
        return get_calculated_totals(monies_data)

    @classmethod
    def get_month_for_user(cls, user_id: int):
        monies = MoneyOrm.get_month_by_user_id(user_id)
        monies_data = MoneyRetrieveAllSchema(
            monies=[MoneyRetrieveSchema.parse_obj(i.__dict__) for i in monies]
        )
        return get_calculated_totals(monies_data)

    @classmethod
    def get_all_for_user(cls, user_id: int):
        monies = MoneyOrm.get_all_by_user_id(user_id)
        monies_data = MoneyRetrieveAllSchema(
            monies=[MoneyRetrieveSchema.parse_obj(i.__dict__) for i in monies]
        )
        return get_calculated_totals(monies_data)

    @classmethod
    def create(cls, user_id: int, data: MoneyCreateSchema):
        money = MoneyOrm.create_money(
            user_id,
            type=data.type,
            is_regular=data.is_regular,
            title=data.title,
            amount=data.amount,
            date=date.today()
        )
        return MoneyRetrieveSchema.parse_obj(money.__dict__)

    @classmethod
    def update(cls, money_id: int, data: MoneyCreateSchema):
        try:
            money = MoneyOrm.edit_money(
                money_id,
                data.is_regular,
                data.title,
                data.amount,
                data.type
            )
            return MoneyRetrieveSchema.parse_obj(money.__dict__)
        except MoneyRecordDoesNotExist as e:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, e.message)

    @classmethod
    def delete(cls, money_id: int):
        try:
            MoneyOrm.delete_money(money_id)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        except MoneyRecordDoesNotExist:
            raise HTTPException(status.HTTP_400_BAD_REQUEST)
