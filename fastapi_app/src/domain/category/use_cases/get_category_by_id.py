from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from schemas.categories import CategorySchema


class GetCategoryByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> CategorySchema:
        with self._database.session() as session:
            category = self._repo.get_by_id(session=session, id=category_id)

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Категория с id {category_id} не найдена',
            )

        return CategorySchema.model_validate(obj=category)
