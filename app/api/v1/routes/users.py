"""Маршруты CRUD для работы с ресурсом пользователя."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dao.user import UserDAO
from app.api.exceptions.user import UserNotFoundException

from app.api.v1.models.request import CreateUserRequestModel
from app.api.v1.models.response import UserResponseModel

from app.api.dependencies.dao import get_user_dao
from app.api.dependencies.db import get_db_session



router = APIRouter(prefix='/users', tags=['users', 'Пользователи', 'v1'])



@router.post('/', response_model=UserResponseModel)
async def create_user(
    user: CreateUserRequestModel,
    user_dao: Annotated[UserDAO, Depends(get_user_dao)],
    session: Annotated[AsyncSession, Depends(get_db_session)]
):
    """
    ## Эндпоинт создания нового пользователя.

    Создает запись в БД на основе валидированной схемы `NewUser` и возвращает
    представление созданного пользователя.

    ### Args:
        user (CreateUserRequestModel): Данные для создания пользователя.
        user_dao (UserDAO): Объект доступа к данным пользователя.
        session (AsyncSession): Асинхронная сессия SQLAlchemy для транзакции.

    ### Returns:
        UserResponseModel: Созданный пользователь с идентификатором.
    """
    async with session.begin():
        res = await user_dao.create(user, session)
    return res


@router.get('/', response_model=list[UserResponseModel])
async def get_all(
    user_dao: Annotated[UserDAO, Depends(get_user_dao)],
    session: Annotated[AsyncSession, Depends(get_db_session)]
):
    """
    ## Эндпоинт получения списка пользователей.

    Возвращает все записи пользователей из базы данных.

    ### Args:
        user_dao (UserDAO): Объект доступа к данным пользователя.
        session (AsyncSession): Асинхронная сессия SQLAlchemy для транзакции.

    ### Returns:
        list[UserResponseModel]: Коллекция пользователей.
    """
    async with session.begin():
        res = await user_dao.get_all(session)
    return res


@router.get('/{user_id}', response_model=UserResponseModel)
async def get_by_id(
    user_id: int,
    user_dao: Annotated[UserDAO, Depends(get_user_dao)],
    session: Annotated[AsyncSession, Depends(get_db_session)]
):
    """
    ## Эндпоинт получения пользователя по идентификатору.

    Возвращает пользователя по его `id` или выбрасывает исключение,
    если запись не найдена.

    ### Args:
        user_id (int): Идентификатор искомого пользователя.
        user_dao (UserDAO): Объект доступа к данным пользователя.
        session (AsyncSession): Асинхронная сессия SQLAlchemy для транзакции.

    ### Raises:
        UserNotFoundException: Пользователь с указанным `id` не найден.

    ### Returns:
        UserResponseModel: Найденный пользователь.
    """
    async with session.begin():
        res = await user_dao.get_by_id(user_id, session)
    if not res:
        raise UserNotFoundException(user_id)
    return res