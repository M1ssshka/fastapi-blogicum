from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.infrastructure.database.repositories.base import (
    BaseRepository,
)
from application.infrastructure.database.models.refresh_tokens import (
    RefreshToken,
)
from application.core.exceptions.database_exceptions import (
    RefreshTokenNotFoundException,
)


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    def __init__(self):
        super().__init__(RefreshToken, RefreshTokenNotFoundException)

    async def get_by_token_hash(
        self, session: AsyncSession, token_hash: str
    ) -> RefreshToken:
        query = select(self._model).where(
            self._model.token_hash == token_hash
        )
        token = await session.scalar(query)
        if not token:
            raise RefreshTokenNotFoundException()
        return token

    async def revoke(self, session: AsyncSession, token_id: int) -> None:
        token = await self.get_by_id(session, token_id)
        token.is_revoked = True

    async def revoke_all_for_user(
        self, session: AsyncSession, user_id: int
    ) -> None:
        query = select(self._model).where(
            self._model.user_id == user_id,
            self._model.is_revoked == False,
        )
        tokens = await session.execute(query)
        for token in tokens.scalars().all():
            token.is_revoked = True
