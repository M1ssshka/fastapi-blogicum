import pytest
from httpx import AsyncClient

from application.api.depends import (
    get_get_all_categories_use_case,
    get_get_category_by_id_use_case,
    get_get_category_by_slug_use_case,
    get_create_category_use_case,
    get_update_category_use_case,
    get_delete_category_use_case,
)
from application.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
    CategoryNotFoundBySlugException,
    CategorySlugAlreadyExistsException,
    ForbiddenActionException,
)
from application.schemas.categories import CategorySchema


def make_category():
    return CategorySchema(
        id=1,
        title='Tech',
        description='Tech category',
        slug='tech',
        is_published=True,
        created_at='2024-01-01T00:00:00',
    )


class TestGetAllCategories:
    @pytest.mark.asyncio
    async def test_get_all_categories(
        self, async_client: AsyncClient, override_use_case
    ):
        override_use_case(
            get_get_all_categories_use_case, lambda *args, **kwargs: []
        )
        response = await async_client.get('/categories')
        assert response.status_code == 200
        assert response.json() == []


class TestGetCategoryById:
    @pytest.mark.asyncio
    async def test_get_by_id_success(
        self, async_client: AsyncClient, override_use_case
    ):
        override_use_case(
            get_get_category_by_id_use_case,
            lambda *args, **kwargs: make_category(),
        )
        response = await async_client.get('/category/1')
        assert response.status_code == 200
        assert response.json()['slug'] == 'tech'

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self, async_client: AsyncClient, override_use_case
    ):
        async def mock_get(*args, **kwargs):
            raise CategoryNotFoundByIdException(id=999)

        override_use_case(get_get_category_by_id_use_case, mock_get)
        response = await async_client.get('/category/999')
        assert response.status_code == 404


class TestGetCategoryBySlug:
    @pytest.mark.asyncio
    async def test_get_by_slug_success(
        self, async_client: AsyncClient, override_use_case
    ):
        override_use_case(
            get_get_category_by_slug_use_case,
            lambda *args, **kwargs: make_category(),
        )
        response = await async_client.get('/category/slug/tech')
        assert response.status_code == 200
        assert response.json()['title'] == 'Tech'

    @pytest.mark.asyncio
    async def test_get_by_slug_not_found(
        self, async_client: AsyncClient, override_use_case
    ):
        async def mock_get(*args, **kwargs):
            raise CategoryNotFoundBySlugException(slug='unknown')

        override_use_case(get_get_category_by_slug_use_case, mock_get)
        response = await async_client.get('/category/slug/unknown')
        assert response.status_code == 404


class TestCreateCategory:
    @pytest.mark.asyncio
    async def test_create_success(
        self,
        async_client: AsyncClient,
        override_superuser_auth,
        override_use_case,
    ):
        override_use_case(
            get_create_category_use_case,
            lambda *args, **kwargs: make_category(),
        )
        response = await async_client.post(
            '/category',
            json={
                'title': 'Tech',
                'description': 'Tech category',
                'slug': 'tech',
                'created_at': '2024-01-01T00:00:00',
            },
        )
        assert response.status_code == 201
        assert response.json()['slug'] == 'tech'

    @pytest.mark.asyncio
    async def test_create_forbidden_non_admin(
        self, async_client: AsyncClient, override_auth, override_use_case
    ):
        async def mock_create(*args, **kwargs):
            raise ForbiddenActionException()

        override_use_case(get_create_category_use_case, mock_create)
        response = await async_client.post(
            '/category',
            json={
                'title': 'Tech',
                'description': 'Desc',
                'slug': 'tech',
                'created_at': '2024-01-01T00:00:00',
            },
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_create_duplicate_slug(
        self,
        async_client: AsyncClient,
        override_superuser_auth,
        override_use_case,
    ):
        async def mock_create(*args, **kwargs):
            raise CategorySlugAlreadyExistsException(slug='tech')

        override_use_case(get_create_category_use_case, mock_create)
        response = await async_client.post(
            '/category',
            json={
                'title': 'Tech',
                'description': 'Desc',
                'slug': 'tech',
                'created_at': '2024-01-01T00:00:00',
            },
        )
        assert response.status_code == 409

    @pytest.mark.asyncio
    async def test_create_unauthorized(self, async_client: AsyncClient):
        response = await async_client.post(
            '/category',
            json={
                'title': 'Hack',
                'description': 'Hack',
                'slug': 'hack',
                'created_at': '2024-01-01T00:00:00',
            },
        )
        assert response.status_code == 401


class TestUpdateCategory:
    @pytest.mark.asyncio
    async def test_update_success(
        self,
        async_client: AsyncClient,
        override_superuser_auth,
        override_use_case,
    ):
        async def mock_update(*args, **kwargs):
            return make_category()

        override_use_case(get_update_category_use_case, mock_update)
        response = await async_client.put(
            '/category/1',
            json={
                'title': 'Updated',
                'description': 'Updated',
                'is_published': True,
            },
        )
        assert response.status_code == 200
        assert response.json()['title'] == 'Tech'

    @pytest.mark.asyncio
    async def test_update_not_found(
        self,
        async_client: AsyncClient,
        override_superuser_auth,
        override_use_case,
    ):
        async def mock_update(*args, **kwargs):
            raise CategoryNotFoundByIdException(id=999)

        override_use_case(get_update_category_use_case, mock_update)
        response = await async_client.put(
            '/category/999',
            json={
                'title': 'Nope',
                'description': 'Nope',
                'is_published': True,
            },
        )
        assert response.status_code == 404


class TestDeleteCategory:
    @pytest.mark.asyncio
    async def test_delete_success(
        self,
        async_client: AsyncClient,
        override_superuser_auth,
        override_use_case,
    ):
        override_use_case(
            get_delete_category_use_case, lambda *args, **kwargs: None
        )
        response = await async_client.delete('/category/1')
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_delete_forbidden_non_admin(
        self, async_client: AsyncClient, override_auth, override_use_case
    ):
        async def mock_delete(*args, **kwargs):
            raise ForbiddenActionException()

        override_use_case(get_delete_category_use_case, mock_delete)
        response = await async_client.delete('/category/1')
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_delete_not_found(
        self,
        async_client: AsyncClient,
        override_superuser_auth,
        override_use_case,
    ):
        async def mock_delete(*args, **kwargs):
            raise CategoryNotFoundByIdException(id=999)

        override_use_case(get_delete_category_use_case, mock_delete)
        response = await async_client.delete('/category/999')
        assert response.status_code == 404
