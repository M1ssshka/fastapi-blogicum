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

logger = logging.getLogger(__name__)


class DeleteCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(
        self,
        comment_id: int,
        user_id: int,
        is_staff: bool = False,
        is_superuser: bool = False,
    ) -> bool:
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
                        f'Пользователь {user_id} попытался удалить чужой комментарий {comment_id} '
                        f'(автор: {comment.author_id})'
                    )
                    raise error

                await self._repo.delete(session=session, id=comment_id)
        except CommentNotFoundException:
            logger.error(
                f'Комментарий с id: {comment_id} не найден для удаления'
            )
            raise CommentNotFoundByIdException(id=comment_id)
        return True
