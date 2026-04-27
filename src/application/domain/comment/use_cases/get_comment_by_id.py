from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.comments import CommentRepository
from application.schemas.comments import CommentResponse


class GetCommentByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> CommentResponse:
        with self._database.session() as session:
            comment = self._repo.get_by_id_with_relations(
                session=session, comment_id=comment_id
            )

        return CommentResponse.model_validate(obj=comment)
