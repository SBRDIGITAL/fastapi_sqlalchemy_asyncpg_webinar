"""Зависимости для работы с базой данных.

Предоставляет генератор асинхронных сессий `AsyncSession` через `Depends`.
"""
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import db_connection



async def get_db_session() -> AsyncIterator[AsyncSession]:
    """
    ## Зависимость: Получение сессии БД.

    Генератор асинхронной сессии SQLAlchemy для использования в эндпоинтах.

    ### Yields:
        AsyncSession: Активная сессия для выполнения операций с БД.
    """
    async with db_connection.get_session() as session:
        yield session


# Экспортируемый интерфейс модуля
__all__ = [
    "get_db_session",
]
