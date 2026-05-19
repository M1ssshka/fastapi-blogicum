import logging
from fastapi.responses import FileResponse
import os

from application.core.exceptions.database_exceptions import (
    PostNotFoundException,
)
from application.core.exceptions.domain_exceptions import (
    PostNotFoundByIdException,
    PostHasNoImageException,
)
from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.posts import (
    PostRepository,
)

logger = logging.getLogger(__name__)


class GetPostImageUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> FileResponse:
        async with self._database.session() as session:
            try:
                post = await self._repo.get_by_id(session=session, id=post_id)
            except PostNotFoundException:
                raise PostNotFoundByIdException(id=post_id)

            if not post.image_path:
                raise PostHasNoImageException()

            file_path = post.image_path.lstrip('/')

            if not os.path.exists(file_path):
                raise PostHasNoImageException()

            return FileResponse(file_path)
