from datetime import date

from schemas.money_schema import MoneyRetrieveAllSchema, MoneyRetrieveSchema, MoneyCreateSchema
from utils.money_util import MoneyUtil


class MoneyView:

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
