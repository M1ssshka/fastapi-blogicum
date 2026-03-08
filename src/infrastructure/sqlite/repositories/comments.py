from typing import Type

from sqlalchemy.orm import Session, joinedload

from infrastructure.sqlite.models.comments import Comment


class CommentRepository:
    def __init__(self):
        self._model: Type[Comment] = Comment

    def get(self, session: Session, comment_id: int) -> Comment | None:
        query = session.query(self._model).options(
            joinedload(self._model.author),
            joinedload(self._model.post),
        ).where(self._model.id == comment_id)
        return query.scalar()
