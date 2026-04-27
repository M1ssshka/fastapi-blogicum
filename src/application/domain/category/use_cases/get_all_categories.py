from typing import List

from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.categories import CategoryRepository
from application.schemas.categories import CategorySchema


class GetAllCategoriesUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(
        self, limit: int = 100, offset: int = 0
    ) -> List[CategorySchema]:
        with self._database.session() as session:
            categories = self._repo.get_all(
                session=session, limit=limit, offset=offset
            )

        return [CategorySchema.model_validate(obj=cat) for cat in categories]
