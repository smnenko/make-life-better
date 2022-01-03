import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base


load_dotenv()


DATABASE_URL = (
    f'postgresql+psycopg2://'
    f'{os.getenv("DATABASE_USER")}:{os.getenv("DATABASE_PASSWORD")}'
    f'@{os.getenv("DATABASE_HOST")}:{os.getenv("DATABASE_PORT")}'
    f'/{os.getenv("DATABASE_NAME")}'
)

engine = create_engine(DATABASE_URL)

Base = declarative_base()

