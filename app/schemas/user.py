"""Базовые Pydantic-схемы для пользователя."""

from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class NewUser(BaseModel):
    """
    ## Модель создания пользователя.

    Используется для валидации входных данных при создании пользователя.

    ### Attributes:
        email (EmailStr): Электронная почта.
        full_name (str): Полное имя пользователя.
        is_hidden (bool): Флаг мягкого удаления (скрытия записи).
    """    
    email: EmailStr = Field(..., max_length=255, description='Электронная почта')
    full_name: str = Field(..., description='Полное имя пользователя')
    is_hidden: bool = Field(
        default=False,
        description='Флаг мягкого удаления (скрытия записи).'
    )


class ExistsUser(NewUser):
    """
    ## Модель существующего пользователя.

    Наследует поля создания и добавляет идентификатор и время создания.

    ### Inherits:
        NewUser: Базовые поля пользователя.

    ### Attributes:
        id (int): Уникальный идентификатор в БД.
        created_at (datetime): Время создания записи о пользователе.
    """    
    id: int = Field(..., description='Уникальный идентификатор пользователя в БД')
    created_at: datetime = Field(..., description='Дата и время создания записи о пользователе')

    # Посмотреть документацию и примеры по field_validator и уточнять у ИИ
    # from pydantic import field_validator
    # @field_validator('created_at', mode='after')
    # def check_created_at(data: datetime):
    #     if isinstance(data, datetime):
    #         return data
    #     raise TypeError(
    #         'Поле created_at не соответствует типу данных datetime.'
    #         f'Его тип данных {type(data)}'
    #     )