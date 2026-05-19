import logging

from application.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
)
from application.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
)
from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.categories import (
    CategoryRepository,
)
from application.schemas.categories import CategorySchema

logger = logging.getLogger(__name__)


class GetCategoryByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> CategorySchema:
        try:
            async with self._database.session() as session:
                category = await self._repo.get_by_id(
                    session=session, id=category_id
                )
        except CategoryNotFoundException:
            logger.error(f'Категория с id: {category_id} не найдена')
            raise CategoryNotFoundByIdException(id=category_id)
        return CategorySchema.model_validate(obj=category)
