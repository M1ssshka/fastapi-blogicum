import logging

from application.core.exceptions.database_exceptions import (
    CommentNotFoundException,
)
from application.core.exceptions.domain_exceptions import (
    CommentNotFoundByIdException,
    ForbiddenActionException,
)
from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.comments import (
    CommentRepository,
)
from application.schemas.comments import CommentResponse, CommentUpdate

logger = logging.getLogger(__name__)


class UpdateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(
        self,
        comment_id: int,
        dto: CommentUpdate,
        user_id: int,
        is_staff: bool = False,
        is_superuser: bool = False,
    ) -> CommentResponse:
        try:
            async with self._database.session() as session:
                comment = await self._repo.get_by_id(
                    session=session, id=comment_id
                )

                if not (
                    is_superuser or is_staff or comment.author_id == user_id
                ):
                    error = ForbiddenActionException()
                    logger.error(
                        f'Пользователь {user_id} попытался изменить чужой комментарий {comment_id} '
                        f'(автор: {comment.author_id})'
                    )
                    raise error

                comment = await self._repo.update(
                    session=session,
                    id=comment_id,
                    text=dto.text,
                )

                comment_with_relations = (
                    await self._repo.get_by_id_with_relations(
                        session=session, comment_id=comment.id
                    )
                )
        except CommentNotFoundException:
            logger.error(f'Комментарий с id: {comment_id} не найден для обновления')
            raise CommentNotFoundByIdException(id=comment_id)
        return CommentResponse.model_validate(obj=comment_with_relations)
