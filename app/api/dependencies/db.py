"""Зависимости FastAPI для работы с базой данных.

Предоставляет генератор асинхронных сессий `AsyncSession` через `Depends`.
"""
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import db_connection



async def get_db_session() -> AsyncIterator[AsyncSession]:
    """
    ## Генератор асинхронной сессии БД.

    Использует контекстный менеджер `DbConnection.get_session` и отдаёт сессию
    через `yield`, чтобы FastAPI корректно закрывал соединение после запроса.

    Yields:
        AsyncSession: Активная асинхронная сессия SQLAlchemy.
    """
    async with db_connection.get_session() as session:
        yield session


# Экспортируемый интерфейс модуля
__all__ = [
    "get_db_session",
]
