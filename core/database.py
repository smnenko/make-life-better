import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()


DATABASE_URL = (
    f'postgresql+asyncpg://'
    f'{os.getenv("DATABASE_USER")}:{os.getenv("DATABASE_PASSWORD")}'
    f'@{os.getenv("DATABASE_HOST")}:{os.getenv("DATABASE_PORT")}'
    f'/{os.getenv("DATABASE_NAME")}'
)

engine = create_async_engine(DATABASE_URL, future=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()
