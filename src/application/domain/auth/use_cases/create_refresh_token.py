import hashlib
import logging
import secrets
from datetime import datetime, timedelta, timezone

from application.core.config import settings
from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.refresh_tokens import (
    RefreshTokenRepository,
)

logger = logging.getLogger(__name__)


class CreateRefreshTokenUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = RefreshTokenRepository()

    async def execute(self, user_id: int) -> str:
        raw_token = secrets.token_urlsafe(48)
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        expires_at = datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )

        try:
            async with self._database.session() as session:
                await self._repo.create(
                    session=session,
                    token_hash=token_hash,
                    user_id=user_id,
                    expires_at=expires_at,
                )
        except Exception as e:
            logger.error(
                f'Ошибка при сохранении refresh токена для пользователя {user_id}: {e}'
            )
            raise

        return raw_token
