from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.categories import CategoryRepository
from application.schemas.categories import CategorySchema


class GetCategoryBySlugUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, slug: str) -> CategorySchema:
        async with self._database.session() as session:
            category = await self._repo.get_by_slug(session=session, slug=slug)

        return CategorySchema.model_validate(obj=category)
