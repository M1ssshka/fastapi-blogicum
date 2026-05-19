from typing import List
from application.core.exceptions.domain_exceptions import (
    ForbiddenActionException,
    PostNotFoundByIdException,
    CategoryNotFoundByIdException,
    LocationNotFoundByIdException,
    PostHasNoImageException,
)
from fastapi import (
    APIRouter,
    status,
    HTTPException,
    Depends,
    UploadFile,
    File,
    Query,
)
from fastapi.responses import FileResponse

from application.schemas.posts import (
    PostCreateSchema,
    PostResponseSchema,
    PostImageResponse,
    PostUpdateSchema,
    UserSchema,
)
from application.domain.post.use_cases.get_post_image import (
    GetPostImageUseCase,
)
from application.domain.post.use_cases.get_post_by_id import GetPostByIdUseCase
from application.domain.post.use_cases.create_post import CreatePostUseCase
from application.domain.post.use_cases.add_post_image import (
    AddPostImageUseCase,
)
from application.domain.post.use_cases.update_post import UpdatePostUseCase
from application.domain.post.use_cases.delete_post import DeletePostUseCase
from application.domain.post.use_cases.get_all_posts import GetAllPostsUseCase

from application.api.depends import (
    get_get_post_by_id_use_case,
    get_create_post_use_case,
    get_update_post_use_case,
    get_delete_post_use_case,
    get_get_all_posts_use_case,
    get_add_post_image_use_case,
    get_get_post_image_use_case,
)
from application.services.auth import AuthService
from starlette.status import HTTP_403_FORBIDDEN

router = APIRouter()


@router.get(
    '/posts',
    status_code=status.HTTP_200_OK,
    response_model=List[PostResponseSchema],
)
async def get_all_posts(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    use_case: GetAllPostsUseCase = Depends(get_get_all_posts_use_case),
) -> List[PostResponseSchema]:
    posts = await use_case.execute(limit=limit, offset=offset)
    return posts


@router.get(
    '/post/{post_id}',
    status_code=status.HTTP_200_OK,
    response_model=PostResponseSchema,
)
async def get_post_by_id(
    post_id: int,
    use_case: GetPostByIdUseCase = Depends(get_get_post_by_id_use_case),
) -> PostResponseSchema:
    try:
        post = await use_case.execute(post_id=post_id)
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
    return post


@router.post(
    '/post',
    status_code=status.HTTP_201_CREATED,
    response_model=PostResponseSchema,
)
async def create_post(
    dto: PostCreateSchema,
    current_user: UserSchema = Depends(AuthService.get_current_user),
    use_case: CreatePostUseCase = Depends(get_create_post_use_case),
) -> PostResponseSchema:
    try:
        post = await use_case.execute(dto=dto, author_id=current_user.id)
    except (
        CategoryNotFoundByIdException,
        LocationNotFoundByIdException,
    ) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=exc.get_detail(),
        )
    return post


@router.put(
    '/post/{post_id}',
    status_code=status.HTTP_200_OK,
    response_model=PostResponseSchema,
)
async def update_post(
    post_id: int,
    dto: PostUpdateSchema,
    current_user: UserSchema = Depends(AuthService.get_current_user),
    use_case: UpdatePostUseCase = Depends(get_update_post_use_case),
) -> PostResponseSchema:
    try:
        post = await use_case.execute(
            post_id=post_id,
            dto=dto,
            user_id=current_user.id,
            is_staff=current_user.is_staff,
            is_superuser=current_user.is_superuser,
        )
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.get_detail(),
        )
    except (
        CategoryNotFoundByIdException,
        LocationNotFoundByIdException,
    ) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=exc.get_detail(),
        )
    except ForbiddenActionException as exc:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=exc.get_detail(),
        )
    return post


@router.delete('/post/{post_id}', status_code=status.HTTP_200_OK)
async def delete_post(
    post_id: int,
    current_user: UserSchema = Depends(AuthService.get_current_user),
    use_case: DeletePostUseCase = Depends(get_delete_post_use_case),
) -> dict:
    try:
        await use_case.execute(
            post_id=post_id,
            user_id=current_user.id,
            is_staff=current_user.is_staff,
            is_superuser=current_user.is_superuser,
        )
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
    except ForbiddenActionException as exc:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail=exc.get_detail()
        )
    return {'message': 'Пост успешно удалён'}


@router.get(
    '/image/post/{post_id}',
    status_code=status.HTTP_200_OK,
    response_class=FileResponse,
)
async def get_post_image(
    post_id: int,
    use_case: GetPostImageUseCase = Depends(get_get_post_image_use_case),
) -> FileResponse:
    try:
        return await use_case.execute(post_id=post_id)
    except (PostNotFoundByIdException, PostHasNoImageException) as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )


@router.post(
    '/image/post',
    status_code=status.HTTP_201_CREATED,
    response_model=PostImageResponse,
)
async def add_post_image(
    image: UploadFile = File(...),
    user: UserSchema = Depends(AuthService.get_current_user),
    use_case: AddPostImageUseCase = Depends(get_add_post_image_use_case),
) -> PostImageResponse:
    return await use_case.execute(image=image)
