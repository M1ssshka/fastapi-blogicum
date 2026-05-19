import logging

from application.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
)
from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.categories import (
    CategoryRepository,
)
from application.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
    ForbiddenActionException,
)

logger = logging.getLogger(__name__)


class DeleteCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(
        self, category_id: int, is_superuser: bool = False
    ) -> bool:
        if not is_superuser:
            error = ForbiddenActionException()
            logger.error(
                f'Попытка удалить категорию {category_id} без прав суперпользователя'
            )
            raise error
        try:
            async with self._database.session() as session:
                await self._repo.delete(session=session, id=category_id)
        except CategoryNotFoundException:
            logger.error(
                f'Категория с id: {category_id} не найдена для удаления'
            )
            raise CategoryNotFoundByIdException(id=category_id)
        return True
