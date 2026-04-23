from core.exceptions.domain_exceptions import ForbiddenActionException
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.comments import CommentRepository
from schemas.comments import CommentResponse, CommentUpdate


class UpdateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(
        self,
        comment_id: int,
        dto: CommentUpdate,
        user_id: int,
        is_staff: bool = False,
        is_superuser: bool = False,
    ) -> CommentResponse:
        with self._database.session() as session:
            comment = self._repo.get_by_id(session=session, id=comment_id)

            if not (is_superuser or is_staff or comment.author_id == user_id):
                raise ForbiddenActionException()

            comment = self._repo.update(
                session=session,
                id=comment_id,
                text=dto.text,
            )

            comment_with_relations = self._repo.get_by_id_with_relations(
                session=session, comment_id=comment.id
            )

        return CommentResponse.model_validate(obj=comment_with_relations)
