from sqlalchemy import select, exists
from sqlalchemy.orm import Session

from models.calorie import Dish


class DishRepository:

    def __init__(self, session: Session):
        self.session = session

    async def get_by_id(self, dish_id: int):
        query = select(Dish).where(Dish.id == dish_id)
        return (await self.session.execute(query)).scalar()
