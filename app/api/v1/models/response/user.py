"""Модели ответов для ресурсов пользователя (v1)."""

from app.schemas.user import ExistsUser


class UserResponseModel(ExistsUser):
    """
    ## Модель ответа с данными пользователя.

    Наследует базовую схему `ExistsUser` и используется в эндпоинтах `v1` при
    возврате информации о пользователе.

    ### Inherits:
        ExistsUser: Схема существующего пользователя с `id` и `created_at`.
    """
    pass