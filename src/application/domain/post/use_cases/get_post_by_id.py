from application.core.exceptions.database_exceptions import PostNotFoundException
from application.core.exceptions.domain_exceptions import PostNotFoundByIdException

from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.posts import PostRepository
from application.schemas.posts import PostResponseSchema


class GetPostByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> PostResponseSchema:
        try:
            async with self._database.session() as session:
                post = await self._repo.get_by_id_with_relations(
                    session=session, post_id=post_id
                )
        except PostNotFoundException:
            raise PostNotFoundByIdException(post_id)

        return PostResponseSchema.model_validate(obj=post)
