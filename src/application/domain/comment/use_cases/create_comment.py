import logging
from datetime import datetime, timezone

from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.comments import (
    CommentRepository,
)
from application.infrastructure.database.repositories.posts import (
    PostRepository,
)
from application.schemas.comments import CommentResponse, CommentCreate
from application.core.exceptions.database_exceptions import (
    PostNotFoundException,
)
from application.core.exceptions.domain_exceptions import (
    PostNotFoundByIdException,
)

logger = logging.getLogger(__name__)


class CreateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()
        self._post_repo = PostRepository()

    async def execute(
        self, dto: CommentCreate, author_id: int
    ) -> CommentResponse:
        try:
            async with self._database.session() as session:
                await self._post_repo.get_by_id(session, dto.post_id)

                comment = await self._repo.create(
                    session=session,
                    text=dto.text,
                    is_published=dto.is_published,
                    author_id=author_id,
                    post_id=dto.post_id,
                    created_at=datetime.now(timezone.utc).replace(tzinfo=None),
                )
                await session.flush()
                comment_with_relations = (
                    await self._repo.get_by_id_with_relations(
                        session=session, comment_id=comment.id
                    )
                )
        except PostNotFoundException:
            logger.error(
                f'Пост с id {dto.post_id} не найден для создания комментария'
            )
            raise PostNotFoundByIdException(id=dto.post_id)

        except Exception as e:
            logger.error(f'Ошибка при создании комментария: {e}')
            raise e

        return CommentResponse.model_validate(obj=comment_with_relations)
