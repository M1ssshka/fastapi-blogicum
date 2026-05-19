from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.infrastructure.database.repositories.base import (
    BaseRepository,
)
from application.infrastructure.database.models.users import User
from application.core.exceptions.database_exceptions import (
    UserNotFoundException,
)


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User, UserNotFoundException)

    async def get_by_username(
        self, session: AsyncSession, username: str
    ) -> User:
        query = select(self._model).where(self._model.username == username)
        user = await session.scalar(query)
        if not user:
            raise UserNotFoundException()
        return user

    async def deactivate_user(
        self, session: AsyncSession, username: str
    ) -> User:
        query = select(self._model).where(self._model.username == username)
        user = await session.scalar(query)
        user.is_active = False
        if not user:
            raise UserNotFoundException()
        return user

    async def activate_user(
        self, session: AsyncSession, username: str
    ) -> User:
        query = select(self._model).where(self._model.username == username)
        user = await session.scalar(query)
        if not user:
            raise UserNotFoundException()
        user.is_active = True
        return user

    async def update_user(
        self, session: AsyncSession, user_id: int, update_data: dict
    ) -> User:
        query = select(self._model).where(self._model.id == user_id)
        user = await session.scalar(query)
        if not user:
            raise UserNotFoundException()

        for key, value in update_data.items():
            if value is not None:
                setattr(user, key, value)

        return user
