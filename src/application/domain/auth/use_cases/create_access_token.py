from datetime import datetime, timedelta, timezone

from jose import jwt

from application.core.config import settings


class CreateAccessTokenUseCase:
    async def execute(
        self, username: str, expires_delta: timedelta | None = None
    ) -> str:
        to_encode = {'sub': username}
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )

        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(
            claims=to_encode,
            key=settings.SECRET_AUTH_KEY.get_secret_value(),
            algorithm=settings.AUTH_ALGORITHM,
        )

        return encoded_jwt
