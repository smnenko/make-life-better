from datetime import date

from fastapi import HTTPException, status, Response

from exceptions.money_exceptions import MoneyRecordDoesNotExist
from schemas.money_schema import (
    MoneyCreateSchema,
    MoneyRetrieveAllSchema,
    MoneyRetrieveSchema
)
from utils.money_util import MoneyUtil


class MoneyView:

    @classmethod
    def get(cls, money_id: int):
        money = MoneyUtil.get_by_id(money_id)
        if not money:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                'Money record not found'
            )
        return MoneyRetrieveSchema.parse_obj(money.__dict__)

    @classmethod
    def get_today_for_user(cls, user_id: int):
        monies = MoneyUtil.get_today_by_user_id(user_id)
        monies_data = MoneyRetrieveAllSchema(
            monies=[MoneyRetrieveSchema.parse_obj(i.__dict__) for i in monies]
        )
        return MoneyUtil.get_calculated_totals(monies_data)

    @classmethod
    def get_week_for_user(cls, user_id: int):
        monies = MoneyUtil.get_week_by_user_id(user_id)
        monies_data = MoneyRetrieveAllSchema(
            monies=[MoneyRetrieveSchema.parse_obj(i.__dict__) for i in monies]
        )
        return MoneyUtil.get_calculated_totals(monies_data)

    @classmethod
    def get_month_for_user(cls, user_id: int):
        monies = MoneyUtil.get_month_by_user_id(user_id)
        monies_data = MoneyRetrieveAllSchema(
            monies=[MoneyRetrieveSchema.parse_obj(i.__dict__) for i in monies]
        )
        return MoneyUtil.get_calculated_totals(monies_data)

    @classmethod
    def get_all_for_user(cls, user_id: int):
        monies = MoneyUtil.get_all_by_user_id(user_id)
        monies_data = MoneyRetrieveAllSchema(
            monies=[MoneyRetrieveSchema.parse_obj(i.__dict__) for i in monies]
        )
        return MoneyUtil.get_calculated_totals(monies_data)

    @classmethod
    def create(cls, user_id: int, data: MoneyCreateSchema):
        money = MoneyUtil.create_money(
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
            money = MoneyUtil.edit_money(
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
            MoneyUtil.delete_money(money_id)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        except MoneyRecordDoesNotExist:
            raise HTTPException(status.HTTP_400_BAD_REQUEST)
