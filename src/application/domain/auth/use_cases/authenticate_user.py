import logging

from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.users import UserRepository
from application.schemas.users import UserSchema
from application.resources.auth import verify_password
from application.core.exceptions.database_exceptions import EntityNotFoundException
from application.core.exceptions.domain_exceptions import (
    UserNotFoundByLoginException,
    WrongPasswordException,
)

logger = logging.getLogger(__name__)


class AuthenticateUserUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = UserRepository()

    async def execute(
        self,
        username: str,
        password: str,
    ) -> UserSchema:
        try:
            with self._database.session() as session:
                user = self._repo.get_by_username(
                    session=session, username=username
                )
        except EntityNotFoundException:
            error = UserNotFoundByLoginException(username=username)
            logger.error(f'Попытка входа с несуществующим логином: {username}')
            raise error

        if not verify_password(
            plain_password=password, hashed_password=user.password
        ):
            error = WrongPasswordException()
            logger.error(f'Неверный пароль для пользователя: {username}')
            raise error

        return UserSchema.model_validate(obj=user)
