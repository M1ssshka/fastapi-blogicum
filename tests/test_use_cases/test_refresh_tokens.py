from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest

from application.core.exceptions.domain_exceptions import (
    InvalidRefreshTokenException,
    RefreshTokenExpiredException,
    RefreshTokenRevokedException,
)
from application.domain.auth.use_cases.refresh_tokens import (
    RefreshTokensUseCase,
)
from application.core.config import settings


@pytest.fixture
def use_case():
    return RefreshTokensUseCase()


class FakeStoredToken:
    def __init__(self, *, is_revoked=False, expires_at=None, user_id=1):
        self.id = 1
        self.is_revoked = is_revoked
        self.expires_at = expires_at or (
            datetime.now(timezone.utc) + timedelta(days=30)
        )
        self.user_id = user_id


class FakeUser:
    def __init__(self, id=1, username='testuser'):
        self.id = id
        self.username = username


@pytest.mark.asyncio
async def test_refresh_tokens_success(use_case, fake_session, fake_db):
    stored = FakeStoredToken()
    fake_session.scalar_results = [
        stored,
        FakeUser(),
        type('RefreshToken', (), {'id': 1})(),
    ]

    with (
        patch.object(settings, 'REFRESH_TOKEN_EXPIRE_DAYS', 30),
        patch.object(
            settings.SECRET_AUTH_KEY, 'get_secret_value', return_value='secret'
        ),
    ):
        access_token, refresh_token = await use_case.execute(
            raw_refresh_token='valid-token'
        )

    assert isinstance(access_token, str)
    assert isinstance(refresh_token, str)
    assert access_token.count('.') == 2


@pytest.mark.asyncio
async def test_refresh_tokens_revoked(use_case, fake_session, fake_db):
    stored = FakeStoredToken(is_revoked=True)
    fake_session.scalar_result = stored

    with pytest.raises(RefreshTokenRevokedException):
        await use_case.execute(raw_refresh_token='revoked-token')


@pytest.mark.asyncio
async def test_refresh_tokens_expired(use_case, fake_session, fake_db):
    stored = FakeStoredToken(
        expires_at=datetime.now(timezone.utc) - timedelta(days=1)
    )
    fake_session.scalar_result = stored

    with pytest.raises(RefreshTokenExpiredException):
        await use_case.execute(raw_refresh_token='expired-token')


@pytest.mark.asyncio
async def test_refresh_tokens_invalid(use_case, fake_session, fake_db):
    fake_session.scalar_result = None

    with pytest.raises(InvalidRefreshTokenException):
        await use_case.execute(raw_refresh_token='invalid-token')
