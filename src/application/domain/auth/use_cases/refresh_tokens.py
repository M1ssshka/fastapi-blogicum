import hashlib
import logging
from datetime import datetime, timezone

from application.core.exceptions.database_exceptions import (
    RefreshTokenNotFoundException,
)
from application.core.exceptions.domain_exceptions import (
    InvalidRefreshTokenException,
    RefreshTokenExpiredException,
    RefreshTokenRevokedException,
)
from application.domain.auth.use_cases.create_access_token import (
    CreateAccessTokenUseCase,
)
from application.domain.auth.use_cases.create_refresh_token import (
    CreateRefreshTokenUseCase,
)
from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.refresh_tokens import (
    RefreshTokenRepository,
)
from application.infrastructure.database.repositories.users import (
    UserRepository,
)

logger = logging.getLogger(__name__)


class RefreshTokensUseCase:
    def __init__(self) -> None:
        self._database = database
        self._refresh_repo = RefreshTokenRepository()
        self._user_repo = UserRepository()
        self._create_access_token = CreateAccessTokenUseCase()
        self._create_refresh_token = CreateRefreshTokenUseCase()

    async def execute(self, raw_refresh_token: str) -> tuple[str, str]:
        token_hash = hashlib.sha256(raw_refresh_token.encode()).hexdigest()

        try:
            async with self._database.session() as session:
                stored = await self._refresh_repo.get_by_token_hash(
                    session=session, token_hash=token_hash
                )

                if stored.is_revoked:
                    raise RefreshTokenRevokedException()

                if stored.expires_at.replace(
                    tzinfo=timezone.utc
                ) < datetime.now(timezone.utc):
                    raise RefreshTokenExpiredException()

                user = await self._user_repo.get_by_id(
                    session=session, id=stored.user_id
                )

                stored.is_revoked = True
        except RefreshTokenNotFoundException:
            raise InvalidRefreshTokenException()

        access_token = await self._create_access_token.execute(
            username=user.username
        )
        refresh_token = await self._create_refresh_token.execute(
            user_id=user.id
        )

        return access_token, refresh_token
