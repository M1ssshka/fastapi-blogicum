from datetime import datetime
from fastapi import APIRouter, status, HTTPException, Depends

from schemas.comments import CommentResponse

from domain.comment.use_cases.get_comment_by_id import GetCommentByIdUseCase
from api.depends import (
    get_get_comment_by_id_use_case,
)

router = APIRouter()


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
