from core.exceptions.domain_exceptions import ForbiddenActionException
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.posts import PostRepository


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
        with self._database.session() as session:
            post = self._repo.get_by_id(session=session, id=post_id)

            if not (is_superuser or is_staff or post.author_id == user_id):
                raise ForbiddenActionException()

            self._repo.delete(session=session, id=post_id)

        return True
