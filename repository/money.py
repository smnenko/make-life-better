from datetime import date

from sqlalchemy.orm import sessionmaker

from core.database import engine
from core.exceptions import ObjectDoesNotExists
from models.money import MoneyRecord
from schemas.money import MoneyCreate

Session = sessionmaker()
Session.configure(bind=engine)


class MoneyRepository:

    session = Session()

    @classmethod
    def get_all_by_user_id(
            cls,
            user_id: int,
            start_date: date = date(1970, 1, 1),
            end_date: date = date.today()
    ):
        return (
            cls
            .session
            .query(MoneyRecord)
            .filter(
                MoneyRecord.user_id == user_id,
                MoneyRecord.date >= start_date,
                MoneyRecord.date <= end_date
            )
            .order_by(MoneyRecord.id.desc())
        )

    @classmethod
    def get_by_id(cls, money_id):
        return cls.session.query(MoneyRecord).filter(MoneyRecord.id == money_id).first()

    @classmethod
    def create_money(cls, user_id: int, money: MoneyCreate):
        money = MoneyRecord(
            user_id=user_id,
            **money.dict(),
            date=date.today()
        )
        cls.session.add(money)
        cls.session.commit()
        cls.session.refresh(money)
        return money

    @classmethod
    def update_money(cls, money: MoneyRecord, data: MoneyCreate):
        money.is_regular = data.is_regular
        money.title = data.title
        money.amount = data.amount
        money.type = data.type

        cls.session.add(money)
        cls.session.commit()
        cls.session.refresh(money)
        return money

    @classmethod
    def delete_money(cls, money: MoneyRecord):
        money = cls.session.query(MoneyRecord).filter(MoneyRecord.id == money.id)
        if not isinstance(money.first(), MoneyRecord):
            raise ObjectDoesNotExists('Money record does\'t exist')

        money.delete()
        cls.session.commit()
