import pytest
from httpx import AsyncClient

from application.api.depends import (
    get_create_user_use_case,
    authenticate_user_use_case,
    create_access_token_use_case,
    create_refresh_token_use_case,
    refresh_tokens_use_case,
)
from application.core.exceptions.domain_exceptions import (
    InvalidRefreshTokenException,
    RefreshTokenExpiredException,
    RefreshTokenRevokedException,
    UserAlreadyExistsException,
    UserNotFoundByLoginException,
    WrongPasswordException,
)
from application.schemas.users import UserResponseSchema


def make_user_response():
    return UserResponseSchema(
        id=1,
        username='testuser',
        first_name='Test',
        last_name='User',
        email='test@example.com',
        is_active=True,
        date_joined='2024-01-01T00:00:00',
    )


class TestLogin:
    @pytest.mark.asyncio
    async def test_login_success(
        self, async_client: AsyncClient, override_use_case
    ):
        async def mock_auth(*args, **kwargs):
            return type(
                'User',
                (),
                {
                    'id': 1,
                    'username': 'testuser',
                    'password': '',
                    'first_name': 'Test',
                    'last_name': 'User',
                    'email': 'test@example.com',
                    'is_staff': False,
                    'is_active': True,
                    'is_superuser': False,
                    'date_joined': '2024-01-01T00:00:00',
                    'last_login': None,
                },
            )()

        async def mock_access(*args, **kwargs):
            return 'mock-access-token'

        async def mock_refresh_create(*args, **kwargs):
            return 'mock-refresh-token'

        override_use_case(authenticate_user_use_case, mock_auth)
        override_use_case(create_access_token_use_case, mock_access)
        override_use_case(create_refresh_token_use_case, mock_refresh_create)

        response = await async_client.post(
            '/token',
            data={'username': 'testuser', 'password': 'correct'},
        )
        assert response.status_code == 200
        data = response.json()
        assert 'access_token' in data
        assert 'refresh_token' in data
        assert data['token_type'] == 'bearer'

    @pytest.mark.asyncio
    async def test_login_wrong_password(
        self, async_client: AsyncClient, override_use_case
    ):
        async def mock_auth(*args, **kwargs):
            raise WrongPasswordException()

        override_use_case(authenticate_user_use_case, mock_auth)

        response = await async_client.post(
            '/token',
            data={'username': 'testuser', 'password': 'wrong'},
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_login_user_not_found(
        self, async_client: AsyncClient, override_use_case
    ):
        async def mock_auth(*args, **kwargs):
            raise UserNotFoundByLoginException(username='ghost')

        override_use_case(authenticate_user_use_case, mock_auth)

        response = await async_client.post(
            '/token',
            data={'username': 'ghost', 'password': 'any'},
        )
        assert response.status_code == 404


class TestRegister:
    @pytest.mark.asyncio
    async def test_register_success(
        self, async_client: AsyncClient, override_use_case
    ):
        async def mock_create(*args, **kwargs):
            return make_user_response()

        override_use_case(get_create_user_use_case, mock_create)

        response = await async_client.post(
            '/register',
            json={
                'username': 'testuser',
                'password': 'strongpass123',
                'email': 'new@example.com',
            },
        )
        assert response.status_code == 201
        assert response.json()['username'] == 'testuser'

    @pytest.mark.asyncio
    async def test_register_duplicate(
        self, async_client: AsyncClient, override_use_case
    ):
        async def mock_create(*args, **kwargs):
            raise UserAlreadyExistsException(username='existing')

        override_use_case(get_create_user_use_case, mock_create)

        response = await async_client.post(
            '/register',
            json={'username': 'existing', 'password': 'strongpass123'},
        )
        assert response.status_code == 409


class TestRefresh:
    @pytest.mark.asyncio
    async def test_refresh_success(
        self, async_client: AsyncClient, override_use_case
    ):
        async def mock_refresh(*args, **kwargs):
            return ('new-access', 'new-refresh')

        override_use_case(refresh_tokens_use_case, mock_refresh)

        response = await async_client.post(
            '/refresh',
            json={'refresh_token': 'valid-refresh-token'},
        )
        assert response.status_code == 200
        data = response.json()
        assert data['access_token'] == 'new-access'
        assert data['refresh_token'] == 'new-refresh'
        assert data['token_type'] == 'bearer'

    @pytest.mark.asyncio
    async def test_refresh_invalid(
        self, async_client: AsyncClient, override_use_case
    ):
        async def mock_refresh(*args, **kwargs):
            raise InvalidRefreshTokenException()

        override_use_case(refresh_tokens_use_case, mock_refresh)

        response = await async_client.post(
            '/refresh',
            json={'refresh_token': 'invalid'},
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_refresh_expired(
        self, async_client: AsyncClient, override_use_case
    ):
        async def mock_refresh(*args, **kwargs):
            raise RefreshTokenExpiredException()

        override_use_case(refresh_tokens_use_case, mock_refresh)

        response = await async_client.post(
            '/refresh',
            json={'refresh_token': 'expired'},
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_refresh_revoked(
        self, async_client: AsyncClient, override_use_case
    ):
        async def mock_refresh(*args, **kwargs):
            raise RefreshTokenRevokedException()

        override_use_case(refresh_tokens_use_case, mock_refresh)

        response = await async_client.post(
            '/refresh',
            json={'refresh_token': 'revoked'},
        )
        assert response.status_code == 401
