from datetime import date, timedelta
from decimal import Decimal
from typing import Optional

from sqlalchemy.orm import sessionmaker

from exceptions.money import MoneyRecordDoesNotExist
from core.database import engine
from models.money import Money
from schemas.money import MoneyCreate

Session = sessionmaker()
Session.configure(bind=engine)


class MoneyOrm:

    session = Session()

    @classmethod
    def get_all_by_user_id(cls, user_id: int):
        return (
            cls
            .session
            .query(Money)
            .filter(Money.user_id == user_id)
            .order_by(Money.id.desc())
        )

    @classmethod
    def get_today_by_user_id(cls, user_id: int):
        return (
            cls
            .session
            .query(Money)
            .filter(
                Money.user_id == user_id,
                Money.date == date.today()
            )
            .order_by(Money.id.desc())
        )

    @classmethod
    def get_week_by_user_id(cls, user_id: int):
        return (
            cls
            .session
            .query(Money)
            .filter(
                Money.user_id == user_id,
                Money.date >= date.today() - timedelta(weeks=1)
            )
            .order_by(Money.id.desc())
        )

    @classmethod
    def get_month_by_user_id(cls, user_id: int):
        return (
            cls
            .session
            .query(Money)
            .filter(
                Money.user_id == user_id,
                Money.date >= date.today() - timedelta(days=30)
            )
            .order_by(Money.id.desc())
        )

    @classmethod
    def get_by_id(cls, money_id):
        return cls.session.query(Money).filter(Money.id == money_id).first()

    @classmethod
    def create_money(cls, user_id: int, money: MoneyCreate):
        money = Money(
            user_id=user_id,
            **money.dict(),
            date=date.today()
        )
        cls.session.add(money)
        cls.session.commit()
        cls.session.refresh(money)
        return money

    @classmethod
    def update_money(cls, money: Money, data: MoneyCreate):
        money.is_regular = data.is_regular
        money.title = data.title
        money.amount = data.amount
        money.type = data.type

        cls.session.add(money)
        cls.session.commit()
        cls.session.refresh(money)
        return money

    @classmethod
    def delete_money(cls, money: Money):
        money = cls.session.query(Money).filter(Money.id == money.id)
        if not isinstance(money.first(), Money):
            raise MoneyRecordDoesNotExist('Money record does\'t exist')

        money.delete()
        cls.session.commit()
