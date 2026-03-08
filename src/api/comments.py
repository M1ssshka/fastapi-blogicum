from typing import List
from fastapi import APIRouter, status, Depends, Query
from schemas.comments import CommentResponse, CommentCreate, CommentUpdate

from domain.comment.use_cases.get_comment_by_id import GetCommentByIdUseCase
from domain.comment.use_cases.create_comment import CreateCommentUseCase
from domain.comment.use_cases.update_comment import UpdateCommentUseCase
from domain.comment.use_cases.delete_comment import DeleteCommentUseCase
from domain.comment.use_cases.get_all_comments import GetAllCommentsUseCase

from api.depends import (
    get_get_comment_by_id_use_case,
    get_create_comment_use_case,
    get_update_comment_use_case,
    get_delete_comment_use_case,
    get_get_all_comments_use_case,
)

router = APIRouter()


@router.get('/comments', status_code=status.HTTP_200_OK, response_model=List[CommentResponse])
async def get_all_comments(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    use_case: GetAllCommentsUseCase = Depends(get_get_all_comments_use_case),
) -> List[CommentResponse]:
    comments = await use_case.execute(limit=limit, offset=offset)
    return comments


@router.get('/comment/{comment_id}', status_code=status.HTTP_200_OK, response_model=CommentResponse)
async def get_comment_by_id(
    comment_id: int,
    use_case: GetCommentByIdUseCase = Depends(get_get_comment_by_id_use_case),
) -> CommentResponse:
    comment = await use_case.execute(comment_id=comment_id)
    return comment


@router.post('/comment', status_code=status.HTTP_201_CREATED, response_model=CommentResponse)
async def create_comment(
    dto: CommentCreate,
    use_case: CreateCommentUseCase = Depends(get_create_comment_use_case),
) -> CommentResponse:
    comment = await use_case.execute(dto=dto)
    return comment


@router.put('/comment/{comment_id}', status_code=status.HTTP_200_OK, response_model=CommentResponse)
async def update_comment(
    comment_id: int,
    dto: CommentUpdate,
    use_case: UpdateCommentUseCase = Depends(get_update_comment_use_case),
) -> CommentResponse:
    comment = await use_case.execute(comment_id=comment_id, dto=dto)
    return comment


@router.delete('/comment/{comment_id}', status_code=status.HTTP_200_OK)
async def delete_comment(
    comment_id: int,
    use_case: DeleteCommentUseCase = Depends(get_delete_comment_use_case),
) -> dict:
    await use_case.execute(comment_id=comment_id)
    return {'message': 'Комментарий успешно удалён'}
