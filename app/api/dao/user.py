"""DAO для операций с пользователем."""

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseDAO
from app.api.v1.models.request import CreateUserRequestModel
from app.api.v1.models.response import UserResponseModel

from app.database.models import User



class UserDAO(BaseDAO):
    """
    ## DAO для ресурса пользователя.

    Инкапсулирует операции создания и чтения пользователей из БД.

    ### Inherits:
        BaseDAO: Базовый класс DAO-хелперов.
    """
    def __init__(self):
        """
        ## Инициализация DAO пользователя.

        Устанавливает ссылку на модель `User`.
        """
        super().__init__()
        self.model = User

    async def create(self,
        user: CreateUserRequestModel,
        session: AsyncSession
    ) -> UserResponseModel:
        """
        ## Создать пользователя.

        Записывает нового пользователя и возвращает сохранённые данные.

        ### Args:
            user (CreateUserRequestModel): Данные для создания.
            session (AsyncSession): Активная сессия БД.

        ### Returns:
            UserResponseModel: Созданный пользователь.
        """
        stmt = (
            insert(self.model)
            .values(**user.model_dump())
            .returning(self.model)
        )
        res = await session.execute(stmt)
        await session.flush()
        obj = res.scalar_one()
        return UserResponseModel(**self._return_dict_from_obj(obj, self.model))

    async def get_all(self, session: AsyncSession) -> list[UserResponseModel]:
        """
        ## Получить всех пользователей.

        ### Args:
            session (AsyncSession): Активная сессия БД.

        ### Returns:
            list[UserResponseModel]: Коллекция пользователей.
        """
        query = select(self.model)
        res = await session.execute(query)
        objects = res.scalars().all()
        return [
            UserResponseModel(**self._return_dict_from_obj(obj, self.model))
            for obj in objects
        ]
    
    async def get_by_id(
        self,
        user_id: int,
        session: AsyncSession
    ) -> UserResponseModel | None:
        """
        ## Получить пользователя по идентификатору.

        ### Args:
            user_id (int): Идентификатор пользователя.
            session (AsyncSession): Активная сессия БД.

        ### Returns:
            UserResponseModel | None: Пользователь или `None`, если не найден.
        """
        query = select(self.model).where(self.model.id == user_id)
        res = await session.execute(query)
        obj = res.scalar_one_or_none()
        if not obj:
            return None
        return UserResponseModel(**self._return_dict_from_obj(obj, self.model))



user_dao = UserDAO()