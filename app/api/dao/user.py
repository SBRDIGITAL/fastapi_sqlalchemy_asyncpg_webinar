from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseDAO
from app.schemas.user import NewUser, ExistsUser

from app.database.models import User



class UserDAO(BaseDAO):

    def __init__(self):
        super().__init__()
        self.model = User

    async def create(self, user: NewUser, session: AsyncSession) -> ExistsUser:
        stmt = (
            insert(self.model)
            .values(**user.model_dump())
            .returning(self.model)
        )
        res = await session.execute(stmt)
        await session.flush()
        obj = res.scalar_one()
        return ExistsUser(**self._return_dict_from_obj(obj, self.model))

    async def get_all(self, session: AsyncSession) -> list[ExistsUser]:
        query = (
            select(self.model)
        )
        res = await session.execute(query)
        # scalars() возвращает чистые ORM-объекты, а не Row, поэтому getattr работает по колонкам
        objects = res.scalars().all()
        return [
            ExistsUser(**self._return_dict_from_obj(obj, self.model))
            for obj in objects
        ]
    
    async def get_by_id(self,
        user_id: int,
        session: AsyncSession
    ) -> ExistsUser | None:
        query = (
            select(self.model)
            .where(self.model.id == user_id)
        )
        res = await session.execute(query)
        obj = res.scalar_one_or_none()
        if not obj:
            return None
        return ExistsUser(**self._return_dict_from_obj(obj, self.model))


user_dao = UserDAO()