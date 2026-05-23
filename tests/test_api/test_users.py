import pytest
from httpx import AsyncClient

from application.api.depends import (
    get_get_user_by_username_use_case,
    get_deactivate_user_use_case,
    get_update_user_use_case,
)
from application.core.exceptions.domain_exceptions import (
    ForbiddenActionException,
    UserNotFoundByLoginException,
)
from application.schemas.users import UserSchema


def make_user(username='target', is_active=True):
    return UserSchema(
        id=1,
        username=username,
        password='hash',
        first_name='Target',
        last_name='User',
        email='t@example.com',
        is_staff=False,
        is_active=is_active,
        is_superuser=False,
        date_joined='2024-01-01T00:00:00',
        last_login=None,
    )


class TestGetUserByUsername:
    @pytest.mark.asyncio
    async def test_get_user_success(
        self, async_client: AsyncClient, override_auth, override_use_case
    ):
        override_use_case(
            get_get_user_by_username_use_case,
            lambda *args, **kwargs: make_user(),
        )

        response = await async_client.get('/user/create/target')
        assert response.status_code == 200
        assert response.json()['username'] == 'target'

    @pytest.mark.asyncio
    async def test_get_user_not_found(
        self, async_client: AsyncClient, override_auth, override_use_case
    ):
        async def mock_get(*args, **kwargs):
            raise UserNotFoundByLoginException(username='ghost')

        override_use_case(get_get_user_by_username_use_case, mock_get)

        response = await async_client.get('/user/create/ghost')
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_user_unauthorized(self, async_client: AsyncClient):
        response = await async_client.get('/user/create/test')
        assert response.status_code == 401


class TestDeactivateUser:
    @pytest.mark.asyncio
    async def test_deactivate_self(
        self, async_client: AsyncClient, override_auth, override_use_case
    ):
        override_use_case(
            get_deactivate_user_use_case,
            lambda *args, **kwargs: make_user(is_active=False),
        )

        response = await async_client.post('/user/deactivate/testuser')
        assert response.status_code == 200
        assert response.json()['is_active'] is False

    @pytest.mark.asyncio
    async def test_deactivate_unauthorized(self, async_client: AsyncClient):
        response = await async_client.post('/user/deactivate/test')
        assert response.status_code == 401


class TestEditUser:
    @pytest.mark.asyncio
    async def test_edit_success(
        self, async_client: AsyncClient, override_auth, override_use_case
    ):
        async def mock_update(*args, **kwargs):
            return make_user(username='testuser')

        override_use_case(get_update_user_use_case, mock_update)

        response = await async_client.put(
            '/user/edit',
            json={'first_name': 'Updated', 'email': 'updated@example.com'},
        )
        assert response.status_code == 200
        assert response.json()['username'] == 'testuser'

    @pytest.mark.asyncio
    async def test_edit_forbidden(
        self, async_client: AsyncClient, override_auth, override_use_case
    ):
        async def mock_update(*args, **kwargs):
            raise ForbiddenActionException()

        override_use_case(get_update_user_use_case, mock_update)

        response = await async_client.put(
            '/user/edit', json={'first_name': 'Hacker'}
        )
        assert response.status_code == 403
