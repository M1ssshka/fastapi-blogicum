from unittest.mock import patch

import pytest

from application.domain.auth.use_cases.create_access_token import (
    CreateAccessTokenUseCase,
)


@pytest.fixture
def use_case():
    return CreateAccessTokenUseCase()


@pytest.mark.asyncio
async def test_create_access_token_success(use_case):
    with patch(
        'application.domain.auth.use_cases.create_access_token.settings.SECRET_AUTH_KEY.get_secret_value',
        return_value='test-secret',
    ):
        token = await use_case.execute(username='testuser')

    assert isinstance(token, str)
    assert len(token) > 0
    assert token.count('.') == 2
