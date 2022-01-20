from datetime import date, timedelta
from typing import Optional

from sqlalchemy.orm import sessionmaker, joinedload

from core.database import engine
from core.exceptions import ObjectDoesNotExists
from models.calorie import CalorieRecord
from schemas.calorie import CalorieCreate, Calorie


Session = sessionmaker()
Session.configure(bind=engine)


class CalorieOrm:

    session = Session()

    @classmethod
    def get_all_by_user_id(
            cls,
            user_id: int,
            start_date: Optional[date] = date(1970, 1, 1),
            end_date: Optional[date] = date.today()
    ):
        return (
            cls
            .session
            .query(CalorieRecord)
            .options(joinedload('dish'))
            .filter(
                CalorieRecord.user_id == user_id,
                CalorieRecord.date >= start_date,
                CalorieRecord.date <= end_date
            )
            .order_by(CalorieRecord.date.asc())
            .all()
        )

    @classmethod
    def get_by_id(cls, calorie_id):
        return (
            cls
            .session
            .query(CalorieRecord.id == calorie_id)
            .first()
        )

    @classmethod
    def create_calorie(cls, user_id: int, calorie: CalorieCreate):
        calorie = CalorieRecord(
            user_id=user_id,
            dish_id=calorie.dish_id,
            amount=calorie.amount,
            date=date.today()
        )

        cls.session.add(calorie)
        cls.session.commit()
        cls.session.refresh(calorie)
        return calorie

    @classmethod
    def update_calorie(cls, calorie: CalorieRecord, data: CalorieCreate):
        calorie.dish_id = data.dish_id
        calorie.amount = data.amount

        cls.session.add(calorie)
        cls.session.commit()
        cls.session.refresh(calorie)
        return calorie

    @classmethod
    def delete_calorie(cls, calorie: CalorieRecord):
        calorie = cls.session.query(Calorie).filter(Calorie.id == calorie.id)

        if not isinstance(calorie.first(), Calorie):
            raise ObjectDoesNotExists('Calorie Record doesn\'t exists')

        calorie.delete()
        cls.session.commit()