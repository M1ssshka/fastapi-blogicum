import logging
from typing import List

from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.posts import (
    PostRepository,
)
from application.schemas.posts import PostResponseSchema

logger = logging.getLogger(__name__)


class GetAllPostsUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(
        self, limit: int = 100, offset: int = 0
    ) -> List[PostResponseSchema]:
        try:
            async with self._database.session() as session:
                posts = await self._repo.get_all(
                    session=session, limit=limit, offset=offset
                )
        except Exception as e:
            logger.error(f'Ошибка при получении списка постов: {e}')
            raise e

        return [PostResponseSchema.model_validate(obj=post) for post in posts]
