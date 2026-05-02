import logging

from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.users import (
    UserRepository,
)
from application.schemas.users import UserSchema
from application.core.exceptions.database_exceptions import (
    UserNotFoundException,
)
from application.core.exceptions.domain_exceptions import (
    UserNotFoundByLoginException,
)

logger = logging.getLogger(__name__)

class GetUserByUsernameUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, username: str) -> UserSchema:
        try:
            async with self._database.session() as session:
                user = await self._repo.get_by_username(
                    session=session, username=username
                )
        except UserNotFoundException:
            logger.error(f'Пользователь с логином {username} не найден')
            raise UserNotFoundByLoginException(username=username)

        return UserSchema.model_validate(obj=user)