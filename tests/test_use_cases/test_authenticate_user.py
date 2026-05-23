from unittest.mock import patch
from datetime import datetime, timezone

import pytest

from application.domain.auth.use_cases.authenticate_user import (
    AuthenticateUserUseCase,
)
from application.core.exceptions.domain_exceptions import (
    WrongPasswordException,
    UserNotFoundByLoginException,
)


@pytest.fixture
def use_case():
    return AuthenticateUserUseCase()


@pytest.mark.asyncio
async def test_authenticate_user_success(use_case, fake_session, fake_db):
    fake_session.scalar_result = type(
        'User',
        (),
        {
            'id': 1,
            'username': 'testuser',
            'password': '$2b$12$hashedpassword',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'is_staff': False,
            'is_active': True,
            'is_superuser': False,
            'date_joined': datetime(2024, 1, 1),
            'last_login': None,
        },
    )()

    with patch(
        'application.domain.auth.use_cases.authenticate_user.verify_password',
        return_value=True,
    ):
        result = await use_case.execute(
            username='testuser', password='correct'
        )

    assert result.username == 'testuser'


@pytest.mark.asyncio
async def test_authenticate_user_wrong_password(
    use_case, fake_session, fake_db
):
    fake_session.scalar_result = type(
        'User',
        (),
        {
            'username': 'testuser',
            'password': '$2b$12$hashed',
        },
    )()

    with patch(
        'application.domain.auth.use_cases.authenticate_user.verify_password',
        return_value=False,
    ):
        with pytest.raises(WrongPasswordException):
            await use_case.execute(username='testuser', password='wrong')


@pytest.mark.asyncio
async def test_authenticate_user_not_found(use_case, fake_session, fake_db):
    fake_session.scalar_result = None

    with pytest.raises(UserNotFoundByLoginException):
        await use_case.execute(username='nonexistent', password='any')
