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
from application.schemas.users import UserSchema, UserUpdateSchema
from application.resources.auth import get_password_hash

logger = logging.getLogger(__name__)


class UpdateUserUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = UserRepository()

    async def execute(
        self,
        target_username: str,
        current_user: UserSchema,
        update_data: UserUpdateSchema,
    ) -> UserSchema:
        try:
            async with self._database.session() as session:
                if (
                    not current_user.is_superuser
                    and target_username != current_user.username
                ):
                    logger.error(
                        f'Пользователь {current_user.username} попытался редактировать {target_username}'
                    )
                    raise ForbiddenActionException()

                user = await self._repo.get_by_username(
                    session=session, username=target_username
                )

                data_to_update = update_data.model_dump(exclude_unset=True)

                if not current_user.is_superuser:
                    forbidden_fields = {
                        'is_superuser',
                        'is_staff',
                        'is_active',
                    }
                    data_to_update = {
                        k: v
                        for k, v in data_to_update.items()
                        if k not in forbidden_fields
                    }

                if 'password' in data_to_update:
                    data_to_update['password'] = get_password_hash(
                        data_to_update['password']
                    )

                updated_user = await self._repo.update_user(
                    session=session,
                    user_id=user.id,
                    update_data=data_to_update,
                )

                await session.commit()
                await session.refresh(updated_user)

        except UserNotFoundException:
            logger.error(f'Пользователь с логином {target_username} не найден')
            raise UserNotFoundByLoginException(username=target_username)

        return UserSchema.model_validate(obj=updated_user)
