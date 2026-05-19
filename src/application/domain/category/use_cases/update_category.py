import logging

from application.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
)
from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.categories import (
    CategoryRepository,
)
from application.schemas.categories import CategorySchema, CategoryUpdateSchema
from application.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
    ForbiddenActionException,
)

logger = logging.getLogger(__name__)


class UpdateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(
        self,
        category_id: int,
        dto: CategoryUpdateSchema,
        is_superuser: bool = False,
    ) -> CategorySchema:
        if not is_superuser:
            error = ForbiddenActionException()
            logger.error(
                f'Попытка изменить категорию {category_id} без прав суперпользователя'
            )
            raise error

        try:
            async with self._database.session() as session:
                category = await self._repo.update(
                    session=session,
                    id=category_id,
                    title=dto.title,
                    description=dto.description,
                    is_published=dto.is_published,
                )
        except CategoryNotFoundException:
            logger.error(
                f'Категория с id: {category_id} не найдена для обновления'
            )
            raise CategoryNotFoundByIdException(id=category_id)
        return CategorySchema.model_validate(obj=category)
