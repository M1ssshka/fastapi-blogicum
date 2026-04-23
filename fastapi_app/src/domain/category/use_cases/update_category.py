from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.categories import CategorySchema, CategoryUpdateSchema
from core.exceptions.domain_exceptions import ForbiddenActionException


class UpdateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(
        self, category_id: int, dto: CategoryUpdateSchema, is_superuser: bool = False
    ) -> CategorySchema:
        if not is_superuser:
            raise ForbiddenActionException()
        
        with self._database.session() as session:
            category = self._repo.update(
                session=session,
                id=category_id,
                title=dto.title,
                description=dto.description,
                is_published=dto.is_published,
            )

        return CategorySchema.model_validate(obj=category)
