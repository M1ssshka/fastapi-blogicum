import logging
from datetime import datetime

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.categories import CategorySchema, CategoryCreateSchema
from core.exceptions.database_exceptions import CategorySlugConflictException
from core.exceptions.domain_exceptions import (
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

        with self._database.session() as session:
            try:
                category = self._repo.create(
                    session=session,
                    title=dto.title,
                    description=dto.description,
                    slug=dto.slug,
                    is_published=dto.is_published,
                    created_at=datetime.now(),
                )
            except CategorySlugConflictException:
                raise CategorySlugAlreadyExistsException(dto.slug)

        return CategorySchema.model_validate(obj=category)
