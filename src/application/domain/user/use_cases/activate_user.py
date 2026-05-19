import logging
from application.core.exceptions.database_exceptions import (
    UserNotFoundException,
)
from application.core.exceptions.domain_exceptions import (
    ForbiddenActionException,
    UserNotFoundByLoginException,
)
from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.users import (
    UserRepository,
)
from application.schemas.users import UserSchema

logger = logging.getLogger(__name__)


class ActivateUserUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = UserRepository()

    async def execute(
        self, target_username: str, current_user: UserSchema
    ) -> UserSchema:
        try:
            async with self._database.session() as session:
                if not current_user.is_superuser:
                    logger.error(
                        f'Пользователь {current_user.username} попытался активировать пользователя {target_username} без прав суперюзера'
                    )
                    raise ForbiddenActionException()

                user = await self._repo.activate_user(session, target_username)
        except UserNotFoundException:
            logger.error(f'Пользователь с логином {target_username} не найден')
            raise UserNotFoundByLoginException(username=target_username)

        return UserSchema.model_validate(obj=user)
