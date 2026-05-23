import pytest
from httpx import AsyncClient

from application.api.depends import (
    get_get_all_locations_use_case,
    get_get_location_by_id_use_case,
    get_create_location_use_case,
    get_update_location_use_case,
    get_delete_location_use_case,
)
from application.core.exceptions.domain_exceptions import (
    ForbiddenActionException,
    LocationNameAlreadyExistsException,
    LocationNotFoundByIdException,
)
from application.schemas.locations import LocationSchema

from tests.test_api.base import (
    assert_create_success,
    assert_create_unauthorized,
    assert_delete_forbidden,
    assert_delete_not_found,
    assert_delete_success,
    assert_get_all_empty,
    assert_get_all_with_data,
    assert_get_by_id_not_found,
    assert_get_by_id_success,
    assert_update_not_found,
    assert_update_success,
)


def make_location():
    return LocationSchema(
        id=1,
        name='Moscow',
        is_published=True,
        created_at='2024-01-01T00:00:00',
    )


class TestGetAllLocations:
    @pytest.mark.asyncio
    async def test_get_all_empty(
        self, async_client: AsyncClient, override_use_case
    ):
        await assert_get_all_empty(
            async_client,
            override_use_case,
            get_get_all_locations_use_case,
            '/locations',
        )

    @pytest.mark.asyncio
    async def test_get_all_with_data(
        self, async_client: AsyncClient, override_use_case
    ):
        await assert_get_all_with_data(
            async_client,
            override_use_case,
            get_get_all_locations_use_case,
            '/locations',
            make_location,
        )


class TestGetLocationById:
    @pytest.mark.asyncio
    async def test_get_by_id_success(
        self, async_client: AsyncClient, override_use_case
    ):
        await assert_get_by_id_success(
            async_client,
            override_use_case,
            get_get_location_by_id_use_case,
            '/location/1',
            make_location,
        )

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self, async_client: AsyncClient, override_use_case
    ):
        await assert_get_by_id_not_found(
            async_client,
            override_use_case,
            get_get_location_by_id_use_case,
            '/location/999',
            LocationNotFoundByIdException,
        )


class TestCreateLocation:
    @pytest.mark.asyncio
    async def test_create_success(
        self,
        async_client: AsyncClient,
        override_superuser_auth,
        override_use_case,
    ):
        await assert_create_success(
            async_client,
            override_use_case,
            get_create_location_use_case,
            '/location',
            {'name': 'Moscow'},
            make_location,
        )

    @pytest.mark.asyncio
    async def test_create_duplicate_name(
        self,
        async_client: AsyncClient,
        override_superuser_auth,
        override_use_case,
    ):
        async def mock_create(*args, **kwargs):
            raise LocationNameAlreadyExistsException(name='Moscow')

        override_use_case(get_create_location_use_case, mock_create)
        response = await async_client.post(
            '/location', json={'name': 'Moscow'}
        )
        assert response.status_code == 409

    @pytest.mark.asyncio
    async def test_create_forbidden_non_admin(
        self, async_client: AsyncClient, override_auth, override_use_case
    ):
        async def mock_create(*args, **kwargs):
            raise ForbiddenActionException()

        override_use_case(get_create_location_use_case, mock_create)
        response = await async_client.post(
            '/location', json={'name': 'Moscow'}
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_create_unauthorized(self, async_client: AsyncClient):
        await assert_create_unauthorized(
            async_client, '/location', {'name': 'Hack'}
        )


class TestUpdateLocation:
    @pytest.mark.asyncio
    async def test_update_success(
        self,
        async_client: AsyncClient,
        override_superuser_auth,
        override_use_case,
    ):
        await assert_update_success(
            async_client,
            override_use_case,
            get_update_location_use_case,
            '/location/1',
            {'name': 'SPb', 'is_published': True},
            make_location,
        )

    @pytest.mark.asyncio
    async def test_update_not_found(
        self,
        async_client: AsyncClient,
        override_superuser_auth,
        override_use_case,
    ):
        await assert_update_not_found(
            async_client,
            override_use_case,
            get_update_location_use_case,
            '/location/999',
            {'name': 'Nope', 'is_published': True},
            LocationNotFoundByIdException,
        )


class TestDeleteLocation:
    @pytest.mark.asyncio
    async def test_delete_success(
        self,
        async_client: AsyncClient,
        override_superuser_auth,
        override_use_case,
    ):
        await assert_delete_success(
            async_client,
            override_use_case,
            get_delete_location_use_case,
            '/location/1',
        )

    @pytest.mark.asyncio
    async def test_delete_forbidden(
        self, async_client: AsyncClient, override_auth, override_use_case
    ):
        await assert_delete_forbidden(
            async_client,
            override_use_case,
            get_delete_location_use_case,
            '/location/1',
        )

    @pytest.mark.asyncio
    async def test_delete_not_found(
        self,
        async_client: AsyncClient,
        override_superuser_auth,
        override_use_case,
    ):
        await assert_delete_not_found(
            async_client,
            override_use_case,
            get_delete_location_use_case,
            '/location/999',
            LocationNotFoundByIdException,
        )
