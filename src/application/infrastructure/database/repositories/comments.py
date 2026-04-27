from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from application.infrastructure.database.repositories.base import BaseRepository
from application.infrastructure.database.models.comments import Comment
from application.core.exceptions.domain_exceptions import CommentNotFoundByIdException


class CommentRepository(BaseRepository[Comment]):
    def __init__(self):
        super().__init__(Comment, CommentNotFoundByIdException)

    async def get_all_with_relations(
        self, session: AsyncSession, limit: int = 100, offset: int = 0
    ) -> list[Comment]:
        query = (
            select(self._model)
            .options(
                joinedload(self._model.author),
                joinedload(self._model.post),
            )
            .limit(limit)
            .offset(offset)
        )
        result = await session.execute(query)
        return list(result.scalars().all())

    async def get_by_id_with_relations(
        self, session: AsyncSession, comment_id: int
    ) -> Comment:
        query = (
            select(self._model)
            .options(
                joinedload(self._model.author),
                joinedload(self._model.post),
            )
            .where(self._model.id == comment_id)
        )
        comment = await session.scalar(query)
        if not comment:
            raise CommentNotFoundByIdException(comment_id)
        return comment
