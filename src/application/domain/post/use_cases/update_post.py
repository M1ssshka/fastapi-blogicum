import logging

from application.core.exceptions.database_exceptions import (
    PostNotFoundException,
    CategoryNotFoundException,
    LocationNotFoundException,
)
from application.core.exceptions.domain_exceptions import (
    ForbiddenActionException,
    PostNotFoundByIdException,
    CategoryNotFoundByIdException,
    LocationNotFoundByIdException,
)
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
from application.schemas.posts import PostResponseSchema, PostUpdateSchema

logger = logging.getLogger(__name__)


class UpdatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._category_repo = CategoryRepository()
        self._location_repo = LocationRepository()

    async def execute(
        self,
        post_id: int,
        dto: PostUpdateSchema,
        user_id: int,
        is_staff: bool = False,
        is_superuser: bool = False,
    ) -> PostResponseSchema:

        try:
            async with self._database.session() as session:
                post = await self._repo.get_by_id(session=session, id=post_id)

                if not (is_superuser or is_staff or post.author_id == user_id):
                    error = ForbiddenActionException()
                    logger.error(
                        f'Пользователь {user_id} попытался изменить чужой пост {post_id} '
                        f'(автор: {post.author_id})'
                    )
                    raise error

                if dto.category_id is not None:
                    try:
                        await self._category_repo.get_by_id(
                            session, dto.category_id
                        )
                    except CategoryNotFoundException:
                        logger.error(
                            f'Категория с id {dto.category_id} не найдена для обновления поста {post_id}'
                        )
                        raise CategoryNotFoundByIdException(id=dto.category_id)

                if dto.location_id is not None:
                    try:
                        await self._location_repo.get_by_id(
                            session, dto.location_id
                        )
                    except LocationNotFoundException:
                        logger.error(
                            f'Локация с id {dto.location_id} не найдена для обновления поста {post_id}'
                        )
                        raise LocationNotFoundByIdException(id=dto.location_id)

                post = await self._repo.update(
                    session=session,
                    id=post_id,
                    title=dto.title,
                    text=dto.text,
                    is_published=dto.is_published,
                    category_id=dto.category_id,
                    location_id=dto.location_id,
                    image_path=dto.image_path,
                )

                post_with_relations = (
                    await self._repo.get_by_id_with_relations(
                        session=session, post_id=post.id
                    )
                )
        except PostNotFoundException:
            logger.error(f'Пост с id: {post_id} не найден для обновления')
            raise PostNotFoundByIdException(id=post_id)

        return PostResponseSchema.model_validate(obj=post_with_relations)
