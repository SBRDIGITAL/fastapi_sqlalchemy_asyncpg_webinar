from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dao.user import UserDAO
from app.api.exceptions.user import UserNotFoundException
from app.schemas.user import NewUser, ExistsUser

from app.api.dependencies.dao import get_user_dao
from app.api.dependencies.db import get_db_session



router = APIRouter(prefix='/users', tags=['users', 'Пользователи', 'v1'])



@router.post('/', response_model=ExistsUser)
async def create_user(
    user: NewUser,
    user_dao: Annotated[UserDAO, Depends(get_user_dao)],
    session: Annotated[AsyncSession, Depends(get_db_session)]
):
    """
    ## Ендпоинт создания нового пользователя

    Args:
        user (NewUser): _description_
        user_dao (Annotated[UserDAO, Depends): _description_
        session (Annotated[AsyncSession, Depends): _description_

    Returns:
        _type_: _description_
    """    
    async with session.begin():
        res = await user_dao.create(user, session)
    return res


@router.get('/', response_model=list[ExistsUser])
async def get_all(
    user_dao: Annotated[UserDAO, Depends(get_user_dao)],
    session: Annotated[AsyncSession, Depends(get_db_session)]
):
    """
    ## Ендпоинт получения всех пользователей.

    Args:
        user_dao (Annotated[UserDAO, Depends): _description_
        session (Annotated[AsyncSession, Depends): _description_

    Returns:
        _type_: _description_
    """    
    async with session.begin():
        res = await user_dao.get_all(session)
    return res


@router.get('/{user_id}', response_model=ExistsUser)
async def get_by_id(
    user_id: int,
    user_dao: Annotated[UserDAO, Depends(get_user_dao)],
    session: Annotated[AsyncSession, Depends(get_db_session)]
):
    """
    ## Ендпоинт получения пользователя по идентификатору.

    Args:
        user_id (int): _description_
        user_dao (Annotated[UserDAO, Depends): _description_
        session (Annotated[AsyncSession, Depends): _description_

    Raises:
        UserNotFoundException: _description_

    Returns:
        _type_: _description_
    """    
    async with session.begin():
        res = await user_dao.get_by_id(user_id, session)
    if not res:
        raise UserNotFoundException(user_id)
    return res