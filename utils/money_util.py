from datetime import date
from decimal import Decimal
from typing import Optional

from sqlalchemy.orm import sessionmaker

from models import engine
from models.money_model import Money
from models.user_model import User

Session = sessionmaker()
Session.configure(bind=engine)


class MoneyUtil:

    session = Session()

    @classmethod
    def get_all_by_user_id(cls, user_id: int):
        return cls.session.query(Money).filter(Money.user_id == user_id).all()

    @classmethod
    def create(
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

