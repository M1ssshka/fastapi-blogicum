from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from application.infrastructure.database.repositories.base import BaseRepository
from application.infrastructure.database.models.posts import Post
from application.core.exceptions.domain_exceptions import PostNotFoundByIdException


class PostRepository(BaseRepository[Post]):
    def __init__(self):
        super().__init__(Post, PostNotFoundByIdException)

    async def get_all(
        self, session: AsyncSession, limit: int = 100, offset: int = 0, options: list | None = None
    ) -> list[Post]:
        default_options = [
            joinedload(self._model.author),
            joinedload(self._model.category),
            joinedload(self._model.location),
        ]
        return await super().get_all(session, limit, offset, options or default_options)

    async def get_by_id_with_relations(self, session: AsyncSession, post_id: int) -> Post:
        query = (
            select(self._model)
            .options(
                joinedload(self._model.author),
                joinedload(self._model.category),
                joinedload(self._model.location),
            )
            .where(self._model.id == post_id)
        )
        post = await session.scalar(query)
        if not post:
            raise PostNotFoundByIdException(post_id)
        return post
