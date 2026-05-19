import logging
from typing import List

from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.comments import (
    CommentRepository,
)
from application.schemas.comments import CommentResponse

logger = logging.getLogger(__name__)


class GetAllCommentsUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(
        self, limit: int = 100, offset: int = 0
    ) -> List[CommentResponse]:
        try:
            async with self._database.session() as session:
                comments = await self._repo.get_all_with_relations(
                    session=session, limit=limit, offset=offset
                )
        except Exception as e:
            logger.error(f'Ошибка при получении списка комментариев: {e}')
            raise e

        return [
            CommentResponse.model_validate(obj=comment) for comment in comments
        ]
