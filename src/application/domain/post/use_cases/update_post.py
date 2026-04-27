import logging

from application.core.exceptions.domain_exceptions import ForbiddenActionException
from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.posts import PostRepository
from application.infrastructure.database.repositories.categories import CategoryRepository
from application.infrastructure.database.repositories.locations import LocationRepository
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
        with self._database.session() as session:
            post = self._repo.get_by_id(session=session, id=post_id)

            if not (is_superuser or is_staff or post.author_id == user_id):
                error = ForbiddenActionException()
                logger.error(
                    f'Пользователь {user_id} попытался изменить чужой пост {post_id} '
                    f'(автор: {post.author_id})'
                )
                raise error

            if dto.category_id is not None:
                self._category_repo.get_by_id(session, dto.category_id)

            if dto.location_id is not None:
                self._location_repo.get_by_id(session, dto.location_id)

            post = self._repo.update(
                session=session,
                id=post_id,
                title=dto.title,
                text=dto.text,
                is_published=dto.is_published,
                category_id=dto.category_id,
                location_id=dto.location_id,
            )

            post_with_relations = self._repo.get_by_id_with_relations(
                session=session, post_id=post.id
            )

        return PostResponseSchema.model_validate(obj=post_with_relations)
