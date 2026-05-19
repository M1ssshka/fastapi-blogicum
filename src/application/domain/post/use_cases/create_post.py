import logging
from datetime import datetime, timezone

from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.posts import (
    PostRepository,
)
from application.infrastructure.database.repositories.categories import (
    CategoryRepository,
)
from application.infrastructure.database.repositories.locations import (
    LocationRepository,
)
from application.schemas.posts import PostResponseSchema, PostCreateSchema
from application.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
    LocationNotFoundException,
)
from application.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
    LocationNotFoundByIdException,
)

logger = logging.getLogger(__name__)


class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._category_repo = CategoryRepository()
        self._location_repo = LocationRepository()

    async def execute(
        self, dto: PostCreateSchema, author_id: int
    ) -> PostResponseSchema:
        async with self._database.session() as session:
            if dto.category_id is not None:
                try:
                    await self._category_repo.get_by_id(
                        session, dto.category_id
                    )
                except CategoryNotFoundException:
                    logger.error(
                        f'Категория с id {dto.category_id} не найдена для создания поста'
                    )
                    raise CategoryNotFoundByIdException(id=dto.category_id)

            if dto.location_id is not None:
                try:
                    await self._location_repo.get_by_id(
                        session, dto.location_id
                    )
                except LocationNotFoundException:
                    logger.error(
                        f'Локация с id {dto.location_id} не найдена для создания поста'
                    )
                    raise LocationNotFoundByIdException(id=dto.location_id)

            post = await self._repo.create(
                session=session,
                title=dto.title,
                text=dto.text,
                is_published=dto.is_published,
                created_at=datetime.now(timezone.utc).replace(tzinfo=None),
                pub_date=dto.pub_date.replace(tzinfo=None)
                if dto.pub_date.tzinfo
                else dto.pub_date,
                author_id=author_id,
                category_id=dto.category_id,
                location_id=dto.location_id,
                image_path=dto.image_path or '',
            )
            await session.flush()
            post_with_relations = await self._repo.get_by_id_with_relations(
                session=session, post_id=post.id
            )

        return PostResponseSchema.model_validate(obj=post_with_relations)
