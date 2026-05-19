import logging
from typing import Annotated

from fastapi import Depends
from jose import JWTError, jwt

from application.core.exceptions.auth_exceptions import CredentialsException
from application.core.exceptions.database_exceptions import (
    EntityNotFoundException,
    UserNotFoundException,
)
from application.schemas.users import UserSchema
from application.resources.auth import oauth2_scheme
from application.infrastructure.database.database import (
    database as sqlite_database,
)
from application.infrastructure.database.repositories.users import (
    UserRepository,
)

from application.core.config import settings

logger = logging.getLogger(__name__)


class AuthService:
    @staticmethod
    async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
        _AUTH_EXCEPTION_MESSAGE = 'Невозможно проверить данные авторизации'
        _database: Database = sqlite_database
        _repo: UserRepository = UserRepository()

        try:
            payload = jwt.decode(
                token=token,
                key=settings.SECRET_AUTH_KEY.get_secret_value(),
                algorithms=[settings.AUTH_ALGORITHM],
            )
            username = payload.get('sub')
            if username is None:
                logger.error(
                    'Попытка доступа с невалидным токеном (отсутствует username)'
                )
                raise CredentialsException(detail=_AUTH_EXCEPTION_MESSAGE)
        except JWTError as e:
            logger.error(f'Попытка доступа с невалидным JWT токеном: {str(e)}')
            raise CredentialsException(detail=_AUTH_EXCEPTION_MESSAGE)

        try:
            async with _database.session() as session:
                user = await _repo.get_by_username(
                    session=session, username=username
                )
        except (EntityNotFoundException, UserNotFoundException):
            logger.error(
                f'Попытка доступа с токеном несуществующего пользователя: {username}'
            )
            raise CredentialsException(detail=_AUTH_EXCEPTION_MESSAGE)

        if not user.is_active:
            logger.error(
                f'Попытка доступа с деактивированного аккаунта: {username}'
            )
            raise CredentialsException(
                detail='Ваш аккаунт деактивирован. Обратитесь в поддержку.'
            )

        return UserSchema.model_validate(obj=user)
