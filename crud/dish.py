from sqlalchemy.orm import sessionmaker

from core.database import engine
from models.calorie import Dish

Session = sessionmaker()
Session.configure(bind=engine)


class DishOrm:

    session = Session()

    @classmethod
    def get_by_id(cls, dish_id: int):
        return cls.session.query(Dish).filter(Dish.id == dish_id).first()
