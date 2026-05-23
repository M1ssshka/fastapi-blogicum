from typing import Any, AsyncGenerator
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from application.app import create_app
from application.schemas.users import UserSchema
from application.services.auth import AuthService


@pytest.fixture
def app() -> FastAPI:
    return create_app()


@pytest.fixture
async def async_client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url='http://test/api/v1'
    ) as client:
        yield client


@pytest.fixture
def mock_current_user() -> UserSchema:
    return UserSchema(
        id=1,
        username='testuser',
        password='hashedpassword',
        first_name='Test',
        last_name='User',
        email='test@example.com',
        is_staff=False,
        is_active=True,
        is_superuser=False,
        date_joined='2024-01-01T00:00:00',
        last_login=None,
    )


@pytest.fixture
def mock_superuser() -> UserSchema:
    return UserSchema(
        id=2,
        username='admin',
        password='hashedpassword',
        first_name='Admin',
        last_name='User',
        email='admin@example.com',
        is_staff=True,
        is_active=True,
        is_superuser=True,
        date_joined='2024-01-01T00:00:00',
        last_login=None,
    )


@pytest.fixture
def override_auth(app: FastAPI, mock_current_user: UserSchema):
    async def override():
        return mock_current_user

    app.dependency_overrides[AuthService.get_current_user] = override
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def override_superuser_auth(app: FastAPI, mock_superuser: UserSchema):
    async def override():
        return mock_superuser

    app.dependency_overrides[AuthService.get_current_user] = override
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def override_use_case(app):
    overrides = {}

    def _register(dep_func, side_effect=None):
        async def mock_callable():
            use_case = MagicMock()
            use_case.execute = AsyncMock(side_effect=side_effect)
            return use_case

        overrides[dep_func] = mock_callable
        app.dependency_overrides[dep_func] = mock_callable

    yield _register

    for dep_func in overrides:
        app.dependency_overrides.pop(dep_func, None)
