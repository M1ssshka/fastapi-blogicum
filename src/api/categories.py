from datetime import datetime
from fastapi import APIRouter, status, HTTPException, Depends

from schemas.categories import CategorySchema
from domain.category.use_cases.get_category_by_slug import (
    GetCategoryBySlugUseCase,
)
from api.depends import (
    get_get_category_by_slug_use_case,
)

router = APIRouter()


@router.get(
    '/category/{slug}',
    status_code=status.HTTP_200_OK,
    response_model=CategorySchema,
)
async def get_category_by_slug(
    slug: str,
    use_case: GetCategoryBySlugUseCase = Depends(
        get_get_category_by_slug_use_case
    ),
) -> CategorySchema:
    category = await use_case.execute(slug=slug)

    return category
