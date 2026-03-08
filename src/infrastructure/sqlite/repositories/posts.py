from typing import Type

from sqlalchemy.orm import Session, joinedload

from infrastructure.sqlite.models.posts import Post


class PostRepository:
    def __init__(self):
        self._model: Type[Post] = Post

    def get(self, session: Session, post_id: int) -> Post | None:
        query = session.query(self._model).options(
            joinedload(self._model.author),
            joinedload(self._model.category),
            joinedload(self._model.location),
        ).where(self._model.id == post_id)
        return query.scalar()
