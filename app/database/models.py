"""SQLAlchemy-модели для абстрактного примера User.

ВНИМАНИЕ: Во всех моделях намеренно отсутствует каскадное удаление (cascade delete) для связей и внешних ключей.

Причины отсутствия каскадного удаления:
    - Безопасность данных: каскадное удаление может привести к случайной потере связанных данных при удалении родительской записи.
    - Явное управление: удаление связанных сущностей должно происходить только по явному решению бизнес-логики приложения, а не автоматически на уровне БД.
    - Аудит и восстановление: мягкое удаление (is_hidden) позволяет сохранять историю и восстанавливать данные при необходимости.
    - Предсказуемость: отсутствие каскада делает поведение системы более прозрачным и контролируемым для разработчиков и пользователей.

Если требуется удалить связанные объекты — это должно быть реализовано явно в сервисном слое приложения.
"""

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (
    Boolean, Column, Index, Sequence, TIMESTAMP,  # служебные классы
    BigInteger, String, Text,  # типы данных
    func, # Функции
)



class Base(DeclarativeBase):
    """
    ## Базовый класс моделей `SQLAlchemy` для примера.

    Args:
        DeclarativeBase: Базовый класс для декларативного определения моделей.
    
    Attributes:
        MAX_MIN_INT_64 (int): Максимально отрицательное значение для 64-битного целого числа.
    """
    MAX_MIN_INT_64 = -9223372036854775808


class User(Base):
    """
    ## Пользователь.

    Attributes:
        id (int): Первичный ключ.
        email (str): Уникальный email пользователя.
        full_name (str): Полное имя пользователя.
        is_hidden (bool): Флаг мягкого удаления (скрытия записи).
        orders (_RelationshipDeclared[Any]): Связь с заказами пользователя.
        __table_args__ (tuple): Составные индексы для оптимизации запросов.
    """
    __tablename__ = 'users'

    id = Column(
        BigInteger,
        Sequence('users_id_seq', start=Base.MAX_MIN_INT_64),
        primary_key=True,
        autoincrement=True,
    )
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(Text, nullable=False)
    is_hidden = Column(Boolean, nullable=False, default=False, index=True)

    # Дата создания записи
    created_at = Column(
        TIMESTAMP(timezone=True),
        # default=datetime.now(timezone.utc),  # это выполнение на стороне Python
        server_default=func.now(),  # лучше использовать на стороне сервера
        nullable=False,
    )

    # Дополнительный составной индекс для поиска по is_hidden и email
    __table_args__ = (
        Index('idx_user_email_is_hidden', 'email', 'is_hidden'),
        # Составное уникальное ограничение для email и full_name  ДЛЯ ПРИМЕРА
        # from sqlalchemy import UniqueConstraint
        # UniqueConstraint('email', 'full_name', name='uq_user_email_full_name'),
    )


# Объект метаданны для использования вне модуля
metadata_obj = Base.metadata


# Экспортируемый интерфейс модуля
__all__ = [
    'metadata_obj',
    'User',
]