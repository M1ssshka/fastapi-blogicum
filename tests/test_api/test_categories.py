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
        await assert_get_all_empty(
            async_client,
            override_use_case,
            get_get_all_categories_use_case,
            '/categories',
        )

    @pytest.mark.asyncio
    async def test_get_all_categories_with_data(
        self, async_client: AsyncClient, override_use_case
    ):
        await assert_get_all_with_data(
            async_client,
            override_use_case,
            get_get_all_categories_use_case,
            '/categories',
            make_category,
        )


class TestGetCategoryById:
    @pytest.mark.asyncio
    async def test_get_by_id_success(
        self, async_client: AsyncClient, override_use_case
    ):
        await assert_get_by_id_success(
            async_client,
            override_use_case,
            get_get_category_by_id_use_case,
            '/category/1',
            make_category,
        )

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self, async_client: AsyncClient, override_use_case
    ):
        await assert_get_by_id_not_found(
            async_client,
            override_use_case,
            get_get_category_by_id_use_case,
            '/category/999',
            CategoryNotFoundByIdException,
        )


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
        await assert_create_success(
            async_client,
            override_use_case,
            get_create_category_use_case,
            '/category',
            {
                'title': 'Tech',
                'description': 'Tech category',
                'slug': 'tech',
                'created_at': '2024-01-01T00:00:00',
            },
            make_category,
        )

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
        await assert_create_unauthorized(
            async_client,
            '/category',
            {
                'title': 'Hack',
                'description': 'Hack',
                'slug': 'hack',
                'created_at': '2024-01-01T00:00:00',
            },
        )


class TestUpdateCategory:
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
            get_update_category_use_case,
            '/category/1',
            {
                'title': 'Updated',
                'description': 'Updated',
                'is_published': True,
            },
            make_category,
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
            get_update_category_use_case,
            '/category/999',
            {
                'title': 'Nope',
                'description': 'Nope',
                'is_published': True,
            },
            CategoryNotFoundByIdException,
        )


class TestDeleteCategory:
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
            get_delete_category_use_case,
            '/category/1',
        )

    @pytest.mark.asyncio
    async def test_delete_forbidden_non_admin(
        self, async_client: AsyncClient, override_auth, override_use_case
    ):
        await assert_delete_forbidden(
            async_client,
            override_use_case,
            get_delete_category_use_case,
            '/category/1',
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
            get_delete_category_use_case,
            '/category/999',
            CategoryNotFoundByIdException,
        )
