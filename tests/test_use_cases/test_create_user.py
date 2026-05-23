from unittest.mock import patch
from datetime import datetime

import pytest

from application.domain.user.use_cases.create_user import CreateUserUseCase
from application.core.exceptions.domain_exceptions import (
    UserAlreadyExistsException,
)


@pytest.fixture
def use_case():
    return CreateUserUseCase()


def make_user(id=1, username='newuser'):
    return type(
        'User',
        (),
        {
            'id': id,
            'username': username,
            'password': 'hashed',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'new@example.com',
            'is_staff': False,
            'is_active': True,
            'is_superuser': False,
            'date_joined': datetime(2024, 1, 1),
            'last_login': None,
        },
    )()


@pytest.mark.asyncio
async def test_create_user_success(use_case, fake_session, fake_db):
    user = make_user()
    fake_session.scalar_result = None

    def _refresh(obj):
        obj.id = 1

    fake_session._refresh_callback = _refresh

    with patch(
        'application.domain.user.use_cases.create_user.get_password_hash',
        return_value='hashed',
    ):
        result = await use_case.execute(
            username='newuser',
            password='strongpass123',
            email='new@example.com',
            first_name='New',
            last_name='User',
        )

    assert result.username == 'newuser'
    assert result.id == 1


@pytest.mark.asyncio
async def test_create_user_duplicate(use_case, fake_session, fake_db):
    fake_session.scalar_result = make_user(username='existing')

    with pytest.raises(UserAlreadyExistsException):
        await use_case.execute(
            username='existing',
            password='strongpass123',
        )
