from sqlalchemy.orm import Session, joinedload

from infrastructure.sqlite.repositories.base import BaseRepository
from infrastructure.sqlite.models.posts import Post
from core.exceptions.domain_exceptions import PostNotFoundByIdException


class PostRepository(BaseRepository[Post]):
    def __init__(self):
        super().__init__(Post, PostNotFoundByIdException)

    def get_by_id_with_relations(self, session: Session, post_id: int) -> Post:
        query = (
            session.query(self._model)
            .options(
                joinedload(self._model.author),
                joinedload(self._model.category),
                joinedload(self._model.location),
            )
            .where(self._model.id == post_id)
        )
        post = query.scalar()
        if not post:
            raise PostNotFoundByIdException(post_id)
        return post
