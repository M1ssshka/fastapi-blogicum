from typing import List
from fastapi import APIRouter, HTTPException, status, Depends, Query
from application.schemas.categories import (
    CategorySchema,
    CategoryCreateSchema,
    CategoryUpdateSchema,
)
from application.schemas.base import SlugStr
from application.schemas.users import UserSchema
from application.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
    CategoryNotFoundBySlugException,
    CategorySlugAlreadyExistsException,
    ForbiddenActionException,
)
from application.services.auth import AuthService

from application.domain.category.use_cases.get_category_by_slug import (
    GetCategoryBySlugUseCase,
)
from application.domain.category.use_cases.get_category_by_id import GetCategoryByIdUseCase
from application.domain.category.use_cases.create_category import CreateCategoryUseCase
from application.domain.category.use_cases.update_category import UpdateCategoryUseCase
from application.domain.category.use_cases.delete_category import DeleteCategoryUseCase
from application.domain.category.use_cases.get_all_categories import (
    GetAllCategoriesUseCase,
)

from application.api.depends import (
    get_get_category_by_slug_use_case,
    get_get_category_by_id_use_case,
    get_create_category_use_case,
    get_update_category_use_case,
    get_delete_category_use_case,
    get_get_all_categories_use_case,
)

router = APIRouter()


@router.get(
    '/categories',
    status_code=status.HTTP_200_OK,
    response_model=List[CategorySchema],
)
async def get_all_categories(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    use_case: GetAllCategoriesUseCase = Depends(
        get_get_all_categories_use_case
    ),
) -> List[CategorySchema]:
    categories = await use_case.execute(limit=limit, offset=offset)
    return categories


@router.get(
    '/category/{category_id}',
    status_code=status.HTTP_200_OK,
    response_model=CategorySchema,
)
async def get_category_by_id(
    category_id: int,
    use_case: GetCategoryByIdUseCase = Depends(
        get_get_category_by_id_use_case
    ),
) -> CategorySchema:
    try:
        category = await use_case.execute(category_id=category_id)
    except CategoryNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
    return category


@router.get(
    '/category/slug/{slug}',
    status_code=status.HTTP_200_OK,
    response_model=CategorySchema,
)
async def get_category_by_slug(
    slug: SlugStr,
    use_case: GetCategoryBySlugUseCase = Depends(
        get_get_category_by_slug_use_case
    ),
) -> CategorySchema:
    try:
        category = await use_case.execute(slug=slug)
    except CategoryNotFoundBySlugException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
    return category


@router.post(
    '/category',
    status_code=status.HTTP_201_CREATED,
    response_model=CategorySchema,
)
async def create_category(
    dto: CategoryCreateSchema,
    current_user: UserSchema = Depends(AuthService.get_current_user),
    use_case: CreateCategoryUseCase = Depends(get_create_category_use_case),
) -> CategorySchema:
    try:
        category = await use_case.execute(
            dto=dto, is_superuser=current_user.is_superuser
        )
    except CategorySlugAlreadyExistsException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail()
        )
    except ForbiddenActionException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=exc.get_detail()
        )
    return category


@router.put(
    '/category/{category_id}',
    status_code=status.HTTP_200_OK,
    response_model=CategorySchema,
)
async def update_category(
    category_id: int,
    dto: CategoryUpdateSchema,
    current_user: UserSchema = Depends(AuthService.get_current_user),
    use_case: UpdateCategoryUseCase = Depends(get_update_category_use_case),
) -> CategorySchema:
    try:
        category = await use_case.execute(
            category_id=category_id,
            dto=dto,
            is_superuser=current_user.is_superuser,
        )
    except CategoryNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
    except ForbiddenActionException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=exc.get_detail()
        )
    return category


@router.delete('/category/{category_id}', status_code=status.HTTP_200_OK)
async def delete_category(
    category_id: int,
    current_user: UserSchema = Depends(AuthService.get_current_user),
    use_case: DeleteCategoryUseCase = Depends(get_delete_category_use_case),
) -> dict:
    try:
        await use_case.execute(
            category_id=category_id, is_superuser=current_user.is_superuser
        )
    except CategoryNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
    except ForbiddenActionException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=exc.get_detail()
        )
    return {'message': 'Категория успешно удалена'}
