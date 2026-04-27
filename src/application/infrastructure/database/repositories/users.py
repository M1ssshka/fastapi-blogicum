from sqlalchemy.orm import Session

from application.infrastructure.database.repositories.base import BaseRepository
from application.infrastructure.database.models.users import User
from application.core.exceptions.domain_exceptions import (
    UserNotFoundByIdException,
    UserNotFoundByLoginException,
)


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User, UserNotFoundByIdException)

    def get_by_username(self, session: Session, username: str) -> User:
        user = (
            session.query(self._model)
            .where(self._model.username == username)
            .scalar()
        )
        if not user:
            raise UserNotFoundByLoginException(username)
        return user
