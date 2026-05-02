import logging
from typing import List

from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.categories import CategoryRepository
from application.schemas.categories import CategorySchema

logger = logging.getLogger(__name__)

class GetAllCategoriesUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(
        self, limit: int = 100, offset: int = 0
    ) -> List[CategorySchema]:
        try:
            async with self._database.session() as session:
                categories = await self._repo.get_all(
                    session=session, limit=limit, offset=offset
                )
        except Exception as e:
            logger.error(f'Ошибка при получении списка категорий: {e}')
            raise e

        return [CategorySchema.model_validate(obj=cat) for cat in categories]