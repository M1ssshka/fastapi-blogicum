from datetime import datetime

from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.posts import PostRepository
from application.infrastructure.database.repositories.categories import CategoryRepository
from application.infrastructure.database.repositories.locations import LocationRepository
from application.schemas.posts import PostResponseSchema, PostCreateSchema


class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._category_repo = CategoryRepository()
        self._location_repo = LocationRepository()

    async def execute(
        self, dto: PostCreateSchema, author_id: int
    ) -> PostResponseSchema:
        with self._database.session() as session:
            if dto.category_id is not None:
                self._category_repo.get_by_id(session, dto.category_id)

            if dto.location_id is not None:
                self._location_repo.get_by_id(session, dto.location_id)

            post = self._repo.create(
                session=session,
                title=dto.title,
                text=dto.text,
                is_published=dto.is_published,
                created_at=datetime.now(),
                pub_date=dto.pub_date,
                author_id=author_id,
                category_id=dto.category_id,
                location_id=dto.location_id,
                image=dto.image or '',
            )
            session.flush()
            post_with_relations = self._repo.get_by_id_with_relations(
                session=session, post_id=post.id
            )

        return PostResponseSchema.model_validate(obj=post_with_relations)
