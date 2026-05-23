import logging

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

            data = dto.model_dump()
            data['author_id'] = author_id
            if data['pub_date'] and data['pub_date'].tzinfo:
                data['pub_date'] = data['pub_date'].replace(tzinfo=None)
            post = await self._repo.create(session=session, **data)
            await session.flush()
            post_with_relations = await self._repo.get_by_id_with_relations(
                session=session, post_id=post.id
            )

        return PostResponseSchema.model_validate(obj=post_with_relations)
