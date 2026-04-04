from datetime import datetime

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.categories import CategorySchema, CategoryCreateSchema
from core.exceptions.database_exceptions import CategorySlugConflictException
from core.exceptions.domain_exceptions import CategorySlugAlreadyExistsException


class CreateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, dto: CategoryCreateSchema) -> CategorySchema:
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
