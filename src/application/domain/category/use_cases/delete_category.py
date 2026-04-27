import logging

from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.categories import CategoryRepository
from application.core.exceptions.domain_exceptions import ForbiddenActionException

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

        with self._database.session() as session:
            self._repo.delete(session=session, id=category_id)

        return True
