from datetime import date
from decimal import Decimal
from typing import Optional

from sqlalchemy.orm import sessionmaker

from models import engine
from models.money_model import Money

Session = sessionmaker()
Session.configure(bind=engine)


class MoneyUtil:

    session = Session()

    @classmethod
    def get_all_by_user_id(cls, user_id: int):
        return cls.session.query(Money).filter(Money.user_id == user_id).all()

    @classmethod
    def create_money(
            cls,
            user_id: int,
            type: int,
            is_regular: bool,
            title: str,
            amount: Decimal,
            date: Optional[date]
    ):
        money = Money(
            user_id=user_id,
            type=type,
            is_regular=is_regular,
            title=title,
            amount=amount,
            date=date
        )
        cls.session.add(money)
        cls.session.commit()
        return money

    @classmethod
    def edit_money(
            cls,
            money_id: int,
            is_regular: bool,
            title: str,
            amount: Decimal
    ):
        money = cls.session.query(Money).filter(Money.id == money_id).first()
        if not isinstance(money, Money):
            raise MoneyRecordDoesNotExist('Money record does\'t exist')

        money.is_regular = is_regular
        money.title = title
        money.amount = amount

        cls.session.add(money)
        cls.session.commit()
        cls.session.refresh(money)
        return money

    @classmethod
    def delete_money(cls, money_id: int):
        money = cls.session.query(Money).filter(Money.id == money_id)
        if not isinstance(money.first(), Money):
            raise MoneyRecordDoesNotExist('Money record does\'t exist')

        money.delete()
        cls.session.commit()
