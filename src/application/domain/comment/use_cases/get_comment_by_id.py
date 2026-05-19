import logging

from application.core.exceptions.domain_exceptions import (
    CommentNotFoundByIdException,
)
from application.core.exceptions.database_exceptions import (
    CommentNotFoundException,
)
from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.comments import (
    CommentRepository,
)
from application.schemas.comments import CommentResponse

logger = logging.getLogger(__name__)


class GetCommentByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> CommentResponse:
        try:
            async with self._database.session() as session:
                comment = await self._repo.get_by_id_with_relations(
                    session=session, comment_id=comment_id
                )
        except CommentNotFoundException:
            logger.error(f'Комментарий с id: {comment_id} не найден')
            raise CommentNotFoundByIdException(id=comment_id)
        return CommentResponse.model_validate(obj=comment)
