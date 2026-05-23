import pytest
from fastapi import Response
from httpx import AsyncClient

from application.api.depends import (
    get_get_all_posts_use_case,
    get_get_post_by_id_use_case,
    get_create_post_use_case,
    get_update_post_use_case,
    get_delete_post_use_case,
    get_add_post_image_use_case,
    get_get_post_image_use_case,
)
from application.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
    ForbiddenActionException,
    PostHasNoImageException,
    PostNotFoundByIdException,
)
from application.schemas.posts import PostImageResponse, PostResponseSchema


def make_post(id=1, author_id=1):
    return {
        'id': id,
        'title': f'Post {id}',
        'text': 'Content',
        'is_published': True,
        'pub_date': '2024-01-01T00:00:00Z',
        'created_at': '2024-01-01T00:00:00Z',
        'image_path': None,
        'author': {
            'id': author_id,
            'username': 'testuser',
            'password': 'hash',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 't@example.com',
            'is_staff': False,
            'is_active': True,
            'is_superuser': False,
            'date_joined': '2024-01-01T00:00:00',
            'last_login': None,
        },
        'category': None,
        'location': None,
    }


def make_post_response(id=1):
    return PostResponseSchema.model_validate(make_post(id))


class TestGetAllPosts:
    @pytest.mark.asyncio
    async def test_get_all_posts_empty(
        self, async_client: AsyncClient, override_use_case
    ):
        override_use_case(
            get_get_all_posts_use_case, lambda *args, **kwargs: []
        )

        response = await async_client.get('/posts')
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_get_all_posts_with_data(
        self, async_client: AsyncClient, override_use_case
    ):
        override_use_case(
            get_get_all_posts_use_case,
            lambda *args, **kwargs: [make_post_response()],
        )

        response = await async_client.get('/posts')
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['title'] == 'Post 1'


class TestGetPostById:
    @pytest.mark.asyncio
    async def test_get_post_success(
        self, async_client: AsyncClient, override_use_case
    ):
        override_use_case(
            get_get_post_by_id_use_case,
            lambda *args, **kwargs: make_post_response(),
        )

        response = await async_client.get('/post/1')
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_post_not_found(
        self, async_client: AsyncClient, override_use_case
    ):
        async def mock_get(*args, **kwargs):
            raise PostNotFoundByIdException(id=999)

        override_use_case(get_get_post_by_id_use_case, mock_get)

        response = await async_client.get('/post/999')
        assert response.status_code == 404


class TestCreatePost:
    @pytest.mark.asyncio
    async def test_create_post_success(
        self, async_client: AsyncClient, override_auth, override_use_case
    ):
        override_use_case(
            get_create_post_use_case,
            lambda *args, **kwargs: make_post_response(),
        )

        response = await async_client.post(
            '/post',
            json={
                'title': 'New Post',
                'text': 'Content',
                'pub_date': '2024-01-01T00:00:00Z',
            },
        )
        assert response.status_code == 201

    @pytest.mark.asyncio
    async def test_create_post_unauthorized(self, async_client: AsyncClient):
        response = await async_client.post(
            '/post',
            json={
                'title': 'Hack',
                'text': 'Hack',
                'pub_date': '2024-01-01T00:00:00Z',
            },
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_create_post_invalid_category(
        self, async_client: AsyncClient, override_auth, override_use_case
    ):
        async def mock_create(*args, **kwargs):
            raise CategoryNotFoundByIdException(id=999)

        override_use_case(get_create_post_use_case, mock_create)

        response = await async_client.post(
            '/post',
            json={
                'title': 'New Post',
                'text': 'Content',
                'pub_date': '2024-01-01T00:00:00Z',
                'category_id': 999,
            },
        )
        assert response.status_code == 422


class TestUpdatePost:
    @pytest.mark.asyncio
    async def test_update_success(
        self, async_client: AsyncClient, override_auth, override_use_case
    ):
        async def mock_update(*args, **kwargs):
            return make_post_response()

        override_use_case(get_update_post_use_case, mock_update)

        response = await async_client.put('/post/1', json={'title': 'Updated'})
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_update_forbidden(
        self, async_client: AsyncClient, override_auth, override_use_case
    ):
        async def mock_update(*args, **kwargs):
            raise ForbiddenActionException()

        override_use_case(get_update_post_use_case, mock_update)

        response = await async_client.put('/post/1', json={'title': 'Hack'})
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_update_not_found(
        self, async_client: AsyncClient, override_auth, override_use_case
    ):
        async def mock_update(*args, **kwargs):
            raise PostNotFoundByIdException(id=999)

        override_use_case(get_update_post_use_case, mock_update)

        response = await async_client.put('/post/999', json={'title': 'Nope'})
        assert response.status_code == 404


class TestDeletePost:
    @pytest.mark.asyncio
    async def test_delete_success(
        self, async_client: AsyncClient, override_auth, override_use_case
    ):
        override_use_case(
            get_delete_post_use_case, lambda *args, **kwargs: None
        )

        response = await async_client.delete('/post/1')
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_delete_forbidden(
        self, async_client: AsyncClient, override_auth, override_use_case
    ):
        async def mock_delete(*args, **kwargs):
            raise ForbiddenActionException()

        override_use_case(get_delete_post_use_case, mock_delete)

        response = await async_client.delete('/post/1')
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_delete_not_found(
        self, async_client: AsyncClient, override_auth, override_use_case
    ):
        async def mock_delete(*args, **kwargs):
            raise PostNotFoundByIdException(id=999)

        override_use_case(get_delete_post_use_case, mock_delete)

        response = await async_client.delete('/post/999')
        assert response.status_code == 404


class TestGetPostImage:
    @pytest.mark.asyncio
    async def test_get_image_success(
        self, async_client: AsyncClient, override_use_case
    ):
        async def mock_get(*args, **kwargs):
            return Response(
                content=b'fake-image-content', media_type='image/jpeg'
            )

        override_use_case(get_get_post_image_use_case, mock_get)

        response = await async_client.get('/image/post/1')
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_image_post_not_found(
        self, async_client: AsyncClient, override_use_case
    ):
        async def mock_get(*args, **kwargs):
            raise PostNotFoundByIdException(id=999)

        override_use_case(get_get_post_image_use_case, mock_get)

        response = await async_client.get('/image/post/999')
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_image_no_image(
        self, async_client: AsyncClient, override_use_case
    ):
        async def mock_get(*args, **kwargs):
            raise PostHasNoImageException()

        override_use_case(get_get_post_image_use_case, mock_get)

        response = await async_client.get('/image/post/1')
        assert response.status_code == 404


class TestAddPostImage:
    @pytest.mark.asyncio
    async def test_add_image_success(
        self, async_client: AsyncClient, override_auth, override_use_case
    ):
        async def mock_add(*args, **kwargs):
            return PostImageResponse(image_path='/static/images/test.jpg')

        override_use_case(get_add_post_image_use_case, mock_add)

        response = await async_client.post(
            '/image/post',
            files={'image': ('test.jpg', b'fake-image-content', 'image/jpeg')},
        )
        assert response.status_code == 201
        assert response.json()['image_path'] == '/static/images/test.jpg'

    @pytest.mark.asyncio
    async def test_add_image_unauthorized(self, async_client: AsyncClient):
        response = await async_client.post('/image/post')
        assert response.status_code == 401
