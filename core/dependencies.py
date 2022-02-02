from core.database import async_session
from repository.money import MoneyRepository
from repository.user import UserRepository


async def get_user_repository():
    async with async_session() as session:
        yield UserRepository(session)


async def get_money_repository():
    async with async_session() as session:
        yield MoneyRepository(session)
