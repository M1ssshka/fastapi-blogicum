import logging

from application.core.exceptions.database_exceptions import (
    PostNotFoundException,
)
from application.core.exceptions.domain_exceptions import (
    ForbiddenActionException,
    PostNotFoundByIdException,
)
from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.posts import (
    PostRepository,
)

logger = logging.getLogger(__name__)


class DeletePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(
        self,
        post_id: int,
        user_id: int,
        is_staff: bool = False,
        is_superuser: bool = False,
    ) -> bool:

        try:
            async with self._database.session() as session:
                post = await self._repo.get_by_id(session=session, id=post_id)

                if not (is_superuser or is_staff or post.author_id == user_id):
                    error = ForbiddenActionException()
                    logger.error(
                        f'Пользователь {user_id} попытался удалить чужой пост {post_id} '
                        f'(автор: {post.author_id})'
                    )
                    raise error

                await self._repo.delete(session=session, id=post_id)
        except PostNotFoundException:
            logger.error(f'Пост с id: {post_id} не найден для удаления')
            raise PostNotFoundByIdException(id=post_id)
        return True
