import logging
from datetime import datetime, timezone

from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.categories import (
    CategoryRepository,
)
from application.schemas.categories import CategorySchema, CategoryCreateSchema
from application.core.exceptions.database_exceptions import (
    CategorySlugConflictException,
)
from application.core.exceptions.domain_exceptions import (
    CategorySlugAlreadyExistsException,
    ForbiddenActionException,
)

logger = logging.getLogger(__name__)


class CreateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(
        self, dto: CategoryCreateSchema, is_superuser: bool = False
    ) -> CategorySchema:
        if not is_superuser:
            error = ForbiddenActionException()
            logger.error(
                'Попытка создать категорию без прав суперпользователя'
            )
            raise error

        try:
            async with self._database.session() as session:
                category = await self._repo.create(
                    session=session,
                    title=dto.title,
                    description=dto.description,
                    slug=dto.slug,
                    is_published=dto.is_published,
                    created_at=datetime.now(timezone.utc).replace(tzinfo=None),
                )
        except CategorySlugConflictException:
            logger.error(f'Категория с slug {dto.slug} уже существует')
            raise CategorySlugAlreadyExistsException(dto.slug)

        return CategorySchema.model_validate(obj=category)
