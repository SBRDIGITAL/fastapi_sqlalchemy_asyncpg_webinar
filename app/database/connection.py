"""Асинхронное подключение к БД для примера SQLAlchemyExample.

Использует параметры подключения и пула из конфигурации: `db_echo`, `db_pool_size`, `db_max_overflow`.
"""

from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession

from app.config.config_reader import env_config



class DbConnection:
    """
    ## Класс для работы с асинхронными сессиями базы данных.

    Использует глобальный Engine (singleton) и создаёт sessionmaker для управления сессиями.
    Согласно best practices SQLAlchemy, Engine создаётся один раз на уровне модуля,
    а DbConnection может создаваться многократно, используя один и тот же Engine.
    
    """
    def __init__(self, engine: AsyncEngine) -> None:
        """
        ## Инициализирует экземпляр `DbConnection`.
        
        Args:
            engine (AsyncEngine): Если не указан, используется глобальный `_engine`.
        """
        self._engine = engine  # Сохраняем ссылку на движок БД
        self._sessionmaker: async_sessionmaker[AsyncSession] = async_sessionmaker(
            # Создаем фабрику асинхронных сессий, привязанную к нашему движку
            bind=self._engine,   # Движок, к которому будут привязываться все сессии
            class_=AsyncSession,  # Указываем тип сессии - асинхронная AsyncSession (не синхронная Session)
            expire_on_commit=False  # Отключаем автоматическую инвалидацию объектов после commit()
            # Объекты остаются валидными для чтения после транзакции
        )

    async def db_close(self, engine: AsyncEngine) -> None:
        """
        ## Закрывает соединение с базой данных.

        Args:
            engine (AsyncEngine): Экземпляр движка.
        """
        await engine.dispose()

    @asynccontextmanager
    async def get_session(self):
        """
        ## Контекстный менеджер для получения асинхронной сессии.

        Yields:
            AsyncSession: Асинхронная сессия БД.
        """
        async with self._sessionmaker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            # finally:
            #     await session.close()
            # https://chat.qwen.ai/s/dfb67396-c32f-4152-8335-3580f390ceab?fev=0.1.15


# Создаётся один раз при импорте модуля
_engine: AsyncEngine = create_async_engine(
    url=env_config.DATABASE_URL_asyncpg,
    echo=env_config.db_echo,
    pool_size=env_config.db_pool_size,
    max_overflow=env_config.db_max_overflow,
)

# Глобальный экземпляр DbConnection для использования в приложении
db_connection = DbConnection(_engine)


# Экспортируемый интерфейс модуля
__all__ = [
    'db_connection',
    'DbConnection',
]