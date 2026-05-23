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
        override_use_case(
            get_get_all_locations_use_case, lambda *args, **kwargs: []
        )
        response = await async_client.get('/locations')
        assert response.status_code == 200
        assert response.json() == []


class TestGetLocationById:
    @pytest.mark.asyncio
    async def test_get_by_id_success(
        self, async_client: AsyncClient, override_use_case
    ):
        override_use_case(
            get_get_location_by_id_use_case,
            lambda *args, **kwargs: make_location(),
        )
        response = await async_client.get('/location/1')
        assert response.status_code == 200
        assert response.json()['name'] == 'Moscow'

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self, async_client: AsyncClient, override_use_case
    ):
        async def mock_get(*args, **kwargs):
            raise LocationNotFoundByIdException(id=999)

        override_use_case(get_get_location_by_id_use_case, mock_get)
        response = await async_client.get('/location/999')
        assert response.status_code == 404


class TestCreateLocation:
    @pytest.mark.asyncio
    async def test_create_success(
        self,
        async_client: AsyncClient,
        override_superuser_auth,
        override_use_case,
    ):
        override_use_case(
            get_create_location_use_case,
            lambda *args, **kwargs: make_location(),
        )
        response = await async_client.post(
            '/location', json={'name': 'Moscow'}
        )
        assert response.status_code == 201
        assert response.json()['name'] == 'Moscow'

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


class TestUpdateLocation:
    @pytest.mark.asyncio
    async def test_update_success(
        self,
        async_client: AsyncClient,
        override_superuser_auth,
        override_use_case,
    ):
        async def mock_update(*args, **kwargs):
            return make_location()

        override_use_case(get_update_location_use_case, mock_update)
        response = await async_client.put(
            '/location/1',
            json={'name': 'SPb', 'is_published': True},
        )
        assert response.status_code == 200
        assert response.json()['name'] == 'Moscow'

    @pytest.mark.asyncio
    async def test_update_not_found(
        self,
        async_client: AsyncClient,
        override_superuser_auth,
        override_use_case,
    ):
        async def mock_update(*args, **kwargs):
            raise LocationNotFoundByIdException(id=999)

        override_use_case(get_update_location_use_case, mock_update)
        response = await async_client.put(
            '/location/999',
            json={'name': 'Nope', 'is_published': True},
        )
        assert response.status_code == 404


class TestDeleteLocation:
    @pytest.mark.asyncio
    async def test_delete_success(
        self,
        async_client: AsyncClient,
        override_superuser_auth,
        override_use_case,
    ):
        override_use_case(
            get_delete_location_use_case, lambda *args, **kwargs: None
        )
        response = await async_client.delete('/location/1')
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_delete_forbidden(
        self, async_client: AsyncClient, override_auth, override_use_case
    ):
        async def mock_delete(*args, **kwargs):
            raise ForbiddenActionException()

        override_use_case(get_delete_location_use_case, mock_delete)
        response = await async_client.delete('/location/1')
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_delete_not_found(
        self,
        async_client: AsyncClient,
        override_superuser_auth,
        override_use_case,
    ):
        async def mock_delete(*args, **kwargs):
            raise LocationNotFoundByIdException(id=999)

        override_use_case(get_delete_location_use_case, mock_delete)
        response = await async_client.delete('/location/999')
        assert response.status_code == 404
