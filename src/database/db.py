from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.config import settings


engine = create_async_engine(settings.DATABSE_URL_asyncpg, future=True)
session_local = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with session_local() as session:
        yield session



