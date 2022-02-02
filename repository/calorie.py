from datetime import date
from typing import Optional

import sqlalchemy
from sqlalchemy import select
from sqlalchemy.orm import joinedload, Session

from core.exceptions import ObjectDoesNotExists
from repository.dish import DishRepository
from models.calorie import CalorieRecord
from schemas.calorie import CalorieCreate


class CalorieRepository:

    def __init__(self, session: Session):
        self.session = session

    async def get_all_by_user_id(
            self,
            user_id: int,
            start_date: Optional[date],
            end_date: Optional[date]
    ):
        query = (
            select(CalorieRecord)
            .where(
                CalorieRecord.user_id == user_id,
                CalorieRecord.date >= start_date,
                CalorieRecord.date <= end_date
            )
            .options(joinedload('dish'))
            .order_by(CalorieRecord.date.asc())
        )
        return (await self.session.execute(query)).scalars().all()

    async def get_by_id(self, calorie_id: int):
        query = select(CalorieRecord).where(CalorieRecord.id == calorie_id)
        try:
            return (await self.session.execute(query)).scalar()
        except sqlalchemy.exc.NoResultFound:
            raise ObjectDoesNotExists('Calorie record doesn\'t exists')

    async def create_calorie(self, user_id: int, calorie: CalorieCreate):
        try:
            calorie = CalorieRecord(
                user_id=user_id,
                dish_id=calorie.dish_id,
                amount=calorie.amount,
                date=calorie.date
            )

            self.session.add(calorie)
            await self.session.commit()
            await self.session.refresh(calorie)
            return calorie
        except sqlalchemy.exc.IntegrityError:
            await self.session.rollback()
            raise ObjectDoesNotExists('Dish doesn\'t exists')

    async def update_calorie(self, calorie: CalorieRecord, data: CalorieCreate):
        calorie.dish_id = data.dish_id
        calorie.amount = data.amount

        self.session.add(calorie)
        await self.session.commit()
        await self.session.refresh(calorie)
        return calorie

    async def delete_calorie(self, calorie: CalorieRecord):
        await self.session.delete(calorie)
        await self.session.commit()
