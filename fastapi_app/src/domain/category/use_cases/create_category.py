from datetime import datetime

from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.categories import CategorySchema, CategoryCreateSchema


class CreateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, dto: CategoryCreateSchema) -> CategorySchema:
        with self._database.session() as session:
            category = self._repo.create(
                session=session,
                title=dto.title,
                description=dto.description,
                slug=dto.slug,
                is_published=dto.is_published,
                created_at=datetime.now(),
            )
            session.flush()

        return CategorySchema.model_validate(obj=category)
