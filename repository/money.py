from datetime import date
from typing import Optional

import sqlalchemy
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.exceptions import ObjectDoesNotExists
from models.money import MoneyRecord
from schemas.money import MoneyCreate


class MoneyRepository:

    def __init__(self, session: Session):
        self.session = session

    async def get_all_by_user_id(
            self,
            user_id: int,
            start_date: Optional[date],
            end_date: Optional[date]
    ):
        query = (
            select(MoneyRecord)
            .where(
                MoneyRecord.user_id == user_id,
                MoneyRecord.date >= start_date,
                MoneyRecord.date <= end_date
            )
            .order_by(MoneyRecord.id.desc())
        )
        return (await self.session.execute(query)).scalars().all()

    async def get_by_id(self, money_id):
        query = select(MoneyRecord).where(MoneyRecord.id == money_id)
        try:
            return (await self.session.execute(query)).scalar()
        except sqlalchemy.exc.NoResultFound:
            raise ObjectDoesNotExists('Money record doesn\'t exists')

    async def create_money(self, user_id: int, money: MoneyCreate):
        money = MoneyRecord(
            user_id=user_id,
            **money.dict(),
            date=date.today()
        )
        self.session.add(money)
        await self.session.commit()
        await self.session.refresh(money)
        return money

    async def update_money(self, money: MoneyRecord, data: MoneyCreate):
        money.is_regular = data.is_regular
        money.title = data.title
        money.amount = data.amount
        money.type = data.type

        self.session.add(money)
        await self.session.commit()
        await self.session.refresh(money)
        return money

    async def delete_money(self, money: MoneyRecord):
        await self.session.delete(money)
        await self.session.commit()
