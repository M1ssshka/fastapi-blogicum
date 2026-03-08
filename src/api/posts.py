from datetime import datetime
from fastapi import APIRouter, status, HTTPException, Depends

from schemas.categories import CategorySchema
from schemas.posts import (
    PostCreateSchema,
    PostUpdateSchema,
    PostResponseSchema,
)

from schemas.users import UserSchema
from schemas.locations import LocationSchema
from schemas.comments import CommentResponse

from domain.user.use_cases.get_user_by_login import GetUserByLoginUseCase
from domain.user.use_cases.get_category_by_slug import GetCategoryBySlugUseCase
from domain.user.use_cases.get_location_by_id import GetLocationByIdUseCase
from domain.user.use_cases.get_post_by_id import GetPostByIdUseCase
from domain.user.use_cases.get_comment_by_id import GetCommentByIdUseCase
from api.depends import (
    get_get_user_by_login_use_case,
    get_get_category_by_slug_use_case,
    get_get_location_by_id_use_case,
    get_get_post_by_id_use_case,
    get_get_comment_by_id_use_case,
)

router = APIRouter()

# fake_db = []
#
#
# @router.get('/get/{post_id}')
# def get_post(post_id: int):
#     if post_id < len(fake_db):
#         return fake_db[post_id]
#     else:
#         raise HTTPException(
#             detail='Пост не найден',
#             status_code=status.HTTP_404_NOT_FOUND,
#         )
#
#
# @router.post(
#     '/create',
#     status_code=status.HTTP_201_CREATED,
#     response_model=PostResponseSchema,
# )
# def create_post(post: PostCreateSchema) -> dict:
#     response = {
#         'id': len(fake_db),
#         'title': post.title,
#         'text': post.text,
#         'pub_date': post.pub_date,
#         'author': post.author,
#         'location': post.location,
#         'category': post.category,
#         'created_at': datetime.now(),
#         'is_published': post.is_published,
#     }
#     fake_db.append(response)
#     return PostResponseSchema.model_validate(obj=response)
#
#
# @router.put(
#     '/update/{post_id}',
#     status_code=status.HTTP_200_OK,
#     response_model=PostResponseSchema,
# )
# def update_post(post_id: int, post: PostUpdateSchema) -> dict:
#     if post_id >= len(fake_db):
#         raise HTTPException(
#             detail='Пост не найден',
#             status_code=status.HTTP_404_NOT_FOUND,
#         )
#     response = fake_db[post_id]
#     response['title'] = post.title
#     response['text'] = post.text
#     response['location'] = post.location
#     response['category'] = post.category
#     response['is_published'] = post.is_published
#     return PostResponseSchema.model_validate(obj=response)
#
#
# @router.delete('/delete/{post_id}', status_code=status.HTTP_200_OK)
# def delete_post(post_id: int):
#     if post_id >= len(fake_db):
#         raise HTTPException(
#             detail='Пост не найден',
#             status_code=status.HTTP_404_NOT_FOUND,
#         )
#     fake_db.pop(post_id)
#     return {'message': 'Пост успешно удален'}


@router.get(
    '/user/{username}',
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
)
async def get_user_by_login(
    username: str,
    use_case: GetUserByLoginUseCase = Depends(get_get_user_by_login_use_case),
) -> UserSchema:
    user = await use_case.execute(username=username)

    return user


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


@router.get(
    '/location/{location_id}',
    status_code=status.HTTP_200_OK,
    response_model=LocationSchema,
)
async def get_location_by_id(
    location_id: int,
    use_case: GetLocationByIdUseCase = Depends(
        get_get_location_by_id_use_case
    ),
) -> LocationSchema:
    location = await use_case.execute(location_id=location_id)

    return location


@router.get(
    '/post/{post_id}',
    status_code=status.HTTP_200_OK,
    response_model=PostResponseSchema,
)
async def get_post_by_id(
    post_id: int,
    use_case: GetPostByIdUseCase = Depends(get_get_post_by_id_use_case),
) -> PostResponseSchema:
    post = await use_case.execute(post_id=post_id)

    return post


@router.get(
    '/comment/{comment_id}',
    status_code=status.HTTP_200_OK,
    response_model=CommentResponse,
)
async def get_comment_by_id(
    comment_id: int,
    use_case: GetCommentByIdUseCase = Depends(get_get_comment_by_id_use_case),
) -> CommentResponse:
    comment = await use_case.execute(comment_id=comment_id)

    return comment
