from datetime import date, timedelta

from sqlalchemy.orm import sessionmaker

from core.database import engine
from models.calorie import CalorieRecord

Session = sessionmaker()
Session.configure(bind=engine)


class CalorieOrm:

    session = Session()

    @classmethod
    def get_all_by_user_id(cls, user_id: int):
        pass

    @classmethod
    def get_today_by_user_id(cls, user_id: int):
        pass

    @classmethod
    def get_week_by_user_id(cls, user_id: int):
        pass

    @classmethod
    def get_by_id(cls, money_id):
        pass

    @classmethod
    def create_money(cls, user_id: int, money: MoneyCreate):
        pass

    @classmethod
    def update_money(cls, money: Money, data: MoneyCreate):
        pass

    @classmethod
    def delete_money(cls, money: Money):
        pass
