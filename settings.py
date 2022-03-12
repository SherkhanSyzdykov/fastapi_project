import os
from dotenv import load_dotenv


load_dotenv()


# HTTP service config
UVICORN_HOST = os.environ.get('UVICORN_HOST', '0.0.0.0')
UVICORN_PORT = os.environ.get('UVICORN_PORT', 8000)


# Postgresql config
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')
POSTGRES_NAME = os.environ.get('POSTGRES_NAME', 'postgres')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'root')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'secret')


# SQLAlchemy config
SQLALCHEMY_SYNC_URL = f'postgresql+psycopg2://' \
                      f'{POSTGRES_USER}:{POSTGRES_PASSWORD}@' \
                      f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}'
SQLALCHEMY_ASYNC_URL = f'postgresql+asyncpg://' \
                       f'{POSTGRES_USER}:{POSTGRES_PASSWORD}@' \
                       f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}'
SQLALCHEMY_POOL_SIZE = 10
SQLALCHEMY_MAX_OVERFLOW = 10
SQLALCHEMY_ECHO = False
