"""Зависимости для работы с DAO."""

from app.api.dao.user import user_dao, UserDAO



def get_user_dao() -> UserDAO:
    """
    ## Зависимость: Получение экземпляра `UserDAO`.

    Возвращает объект доступа к данным пользователя для использования в эндпоинтах.

    ### Returns:
        UserDAO: Экземпляр DAO для работы с пользователями.
    """
    return user_dao