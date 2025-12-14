from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class NewUser(BaseModel):
    """
    ## Модель нового пользователя

    Args:
        BaseModel (pydantic.BaseModel): ...
    
    Attributes:
        email (EmailStr): ...
        full_name (str): ...
        is_hidden (bool): ...
    """    
    email: EmailStr = Field(..., max_length=255, description='Электронная почта')
    full_name: str = Field(..., description='Полное имя пользователя')
    is_hidden: bool = Field(
        default=False,
        description='Флаг мягкого удаления (скрытия записи).'
    )


class ExistsUser(NewUser):
    """
    ## _summary_

    Args:
        NewUser (_type_): _description_
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