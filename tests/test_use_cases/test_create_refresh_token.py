from unittest.mock import patch

import pytest

from application.domain.auth.use_cases.create_refresh_token import (
    CreateRefreshTokenUseCase,
)


@pytest.fixture
def use_case():
    return CreateRefreshTokenUseCase()


@pytest.mark.asyncio
async def test_create_refresh_token_success(use_case, fake_session, fake_db):
    with patch(
        'application.domain.auth.use_cases.create_refresh_token.settings.REFRESH_TOKEN_EXPIRE_DAYS',
        30,
    ):
        token = await use_case.execute(user_id=1)

    assert isinstance(token, str)
    assert len(token) > 0
