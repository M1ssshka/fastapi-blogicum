from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from application.infrastructure.database.repositories.base import (
    BaseRepository,
)
from application.infrastructure.database.models.categories import Category

from application.core.exceptions.database_exceptions import (
    CategorySlugConflictException,
    CategoryNotFoundException,
)


class CategoryRepository(BaseRepository[Category]):
    def __init__(self):
        super().__init__(Category, CategoryNotFoundException)

    async def get_by_slug(self, session: AsyncSession, slug: str) -> Category:
        query = select(self._model).where(self._model.slug == slug)
        category = await session.scalar(query)
        if not category:
            raise CategoryNotFoundException(slug)
        return category

    async def create(self, session: AsyncSession, **kwargs) -> Category:
        try:
            return await super().create(session=session, **kwargs)
        except IntegrityError:
            raise CategorySlugConflictException()
