from datetime import datetime

from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.comments import CommentRepository
from application.schemas.comments import CommentResponse, CommentCreate


class CreateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(
        self, dto: CommentCreate, author_id: int
    ) -> CommentResponse:
        with self._database.session() as session:
            comment = self._repo.create(
                session=session,
                text=dto.text,
                is_published=dto.is_published,
                author_id=author_id,
                post_id=dto.post_id,
                created_at=datetime.now(),
            )
            session.flush()
            comment_with_relations = self._repo.get_by_id_with_relations(
                session=session, comment_id=comment.id
            )

        return CommentResponse.model_validate(obj=comment_with_relations)
