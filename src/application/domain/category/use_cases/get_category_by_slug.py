import logging

from application.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
)
from application.core.exceptions.domain_exceptions import (
    CategoryNotFoundBySlugException,
)
from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.categories import (
    CategoryRepository,
)
from application.schemas.categories import CategorySchema

logger = logging.getLogger(__name__)


class GetCategoryBySlugUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, slug: str) -> CategorySchema:
        try:
            async with self._database.session() as session:
                category = await self._repo.get_by_slug(
                    session=session, slug=slug
                )
        except CategoryNotFoundException:
            logger.error(f'Категория с slug: {slug} не найдена')
            raise CategoryNotFoundBySlugException(slug=slug)
        return CategorySchema.model_validate(obj=category)
