import pytest
from httpx import AsyncClient

from application.api.depends import (
    get_activate_user_use_case,
    get_deactivate_user_use_case,
    get_update_user_use_case,
)
from application.core.exceptions.domain_exceptions import (
    ForbiddenActionException,
    UserNotFoundByLoginException,
)
from application.schemas.users import UserSchema


def make_user(username='target', is_active=True, is_superuser=False):
    return UserSchema(
        id=2,
        username=username,
        password='hash',
        first_name='Target',
        last_name='User',
        email='t@example.com',
        is_staff=False,
        is_active=is_active,
        is_superuser=is_superuser,
        date_joined='2024-01-01T00:00:00',
        last_login=None,
    )


class TestAdminActivate:
    @pytest.mark.asyncio
    async def test_activate_success(
        self,
        async_client: AsyncClient,
        override_superuser_auth,
        override_use_case,
    ):
        override_use_case(
            get_activate_user_use_case,
            lambda *args, **kwargs: make_user(is_active=True),
        )

        response = await async_client.post('/admin/user/activate/target')
        assert response.status_code == 200
        assert response.json()['is_active'] is True

    @pytest.mark.asyncio
    async def test_activate_forbidden_non_admin(
        self, async_client: AsyncClient, override_auth
    ):
        response = await async_client.post('/admin/user/activate/target')
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_activate_not_found(
        self,
        async_client: AsyncClient,
        override_superuser_auth,
        override_use_case,
    ):
        async def mock_activate(*args, **kwargs):
            raise UserNotFoundByLoginException(username='ghost')

        override_use_case(get_activate_user_use_case, mock_activate)

        response = await async_client.post('/admin/user/activate/ghost')
        assert response.status_code == 404


class TestAdminDeactivate:
    @pytest.mark.asyncio
    async def test_deactivate_success(
        self,
        async_client: AsyncClient,
        override_superuser_auth,
        override_use_case,
    ):
        override_use_case(
            get_deactivate_user_use_case,
            lambda *args, **kwargs: make_user(is_active=False),
        )

        response = await async_client.post('/admin/user/deactivate/target')
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_deactivate_forbidden_non_admin(
        self, async_client: AsyncClient, override_auth
    ):
        response = await async_client.post('/admin/user/deactivate/target')
        assert response.status_code == 403


class TestAdminEdit:
    @pytest.mark.asyncio
    async def test_edit_success(
        self,
        async_client: AsyncClient,
        override_superuser_auth,
        override_use_case,
    ):
        async def mock_update(*args, **kwargs):
            return make_user(is_superuser=True, is_active=True)

        override_use_case(get_update_user_use_case, mock_update)

        response = await async_client.put(
            '/admin/user/edit/target',
            json={
                'first_name': 'Updated',
                'is_superuser': True,
                'is_staff': True,
            },
        )
        assert response.status_code == 200
        assert response.json()['is_superuser'] is True

    @pytest.mark.asyncio
    async def test_edit_forbidden_non_admin(
        self, async_client: AsyncClient, override_auth
    ):
        response = await async_client.put(
            '/admin/user/edit/target',
            json={'first_name': 'Hacker'},
        )
        assert response.status_code == 403
