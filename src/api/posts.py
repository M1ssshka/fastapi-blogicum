from datetime import datetime
from fastapi import APIRouter, status, HTTPException, Depends

from schemas.posts import (
    PostResponseSchema,
)

from domain.post.use_cases.get_post_by_id import GetPostByIdUseCase
from api.depends import (
    get_get_post_by_id_use_case,
)

router = APIRouter()


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
