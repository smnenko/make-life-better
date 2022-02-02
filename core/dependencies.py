from core.database import async_session
from repository.calorie import CalorieRepository
from repository.dish import DishRepository
from repository.money import MoneyRepository
from repository.user import UserRepository


async def get_user_repository():
    async with async_session() as session:
        yield UserRepository(session)


async def get_money_repository():
    async with async_session() as session:
        yield MoneyRepository(session)


async def get_calorie_repository():
    async with async_session() as session:
        yield CalorieRepository(session)


async def get_dish_repository():
    async with async_session() as session:
        yield DishRepository(session)
