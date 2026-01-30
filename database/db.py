"""Подключение к базе данных."""

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from database.models import Base
from config import DATABASE_URL


# Создание асинхронного движка
engine = create_async_engine(DATABASE_URL, echo=False)

# Создание фабрики сессий
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    """Инициализация базы данных (создание таблиц)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ База данных инициализирована")


async def get_session() -> AsyncSession:
    """Получение сессии базы данных."""
    async with async_session() as session:
        yield session
