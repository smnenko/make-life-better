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
        return (
            cls
            .session
            .query(CalorieRecord)
            .filter(CalorieRecord.user_id == user_id)
            .order_by(CalorieRecord.date.asc())
        )

    @classmethod
    def get_today_by_user_id(cls, user_id: int):
        return (
            cls
            .session
            .query(CalorieRecord)
            .filter(
                CalorieRecord.user_id == user_id,
                CalorieRecord.date == date.today()
            ).order_by(CalorieRecord.date.asc())
        )

    @classmethod
    def get_week_by_user_id(cls, user_id: int):
        return (
            cls
            .session
            .query(CalorieRecord)
            .filter(
                CalorieRecord.user_id == user_id,
                CalorieRecord.date >= date.today() - timedelta(weeks=1)
            ).order_by(CalorieRecord.date.asc())
        )

    @classmethod
    def get_by_id(cls, calorie_id):
        return (
            cls
            .session
            .query(CalorieRecord.id == calorie_id)
        )

    @classmethod
    def create_calorie(cls, user_id: int, calorie: MoneyCreate):
        pass

    @classmethod
    def update_money(cls, money: Money, data: MoneyCreate):
        pass

    @classmethod
    def delete_money(cls, money: Money):
        pass
