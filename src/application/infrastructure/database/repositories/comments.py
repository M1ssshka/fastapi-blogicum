from sqlalchemy.orm import Session, joinedload

from application.infrastructure.database.repositories.base import BaseRepository
from application.infrastructure.database.models.comments import Comment
from application.core.exceptions.domain_exceptions import CommentNotFoundByIdException


class CommentRepository(BaseRepository[Comment]):
    def __init__(self):
        super().__init__(Comment, CommentNotFoundByIdException)

    def get_all_with_relations(
        self, session: Session, limit: int = 100, offset: int = 0
    ) -> list[Comment]:
        query = (
            session.query(self._model)
            .options(
                joinedload(self._model.author),
                joinedload(self._model.post),
            )
            .limit(limit)
            .offset(offset)
            .all()
        )
        return query

    def get_by_id_with_relations(
        self, session: Session, comment_id: int
    ) -> Comment:
        query = (
            session.query(self._model)
            .options(
                joinedload(self._model.author),
                joinedload(self._model.post),
            )
            .where(self._model.id == comment_id)
        )
        comment = query.scalar()
        if not comment:
            raise CommentNotFoundByIdException(comment_id)
        return comment
