from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.categories import CategorySchema


class GetCategoryBySlugUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, slug: str) -> CategorySchema:
        with self._database.session() as session:
            category = self._repo.get_by_slug(session=session, slug=slug)

        return CategorySchema.model_validate(obj=category)
