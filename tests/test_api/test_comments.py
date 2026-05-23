import pytest
from httpx import AsyncClient

from application.api.depends import (
    get_get_all_comments_use_case,
    get_get_comment_by_id_use_case,
    get_create_comment_use_case,
    get_update_comment_use_case,
    get_delete_comment_use_case,
)
from application.core.exceptions.domain_exceptions import (
    CommentNotFoundByIdException,
    ForbiddenActionException,
    PostNotFoundByIdException,
)
from application.schemas.comments import CommentResponse


def make_comment_author():
    return {
        'id': 1,
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
    }


def make_comment():
    return CommentResponse(
        id=1,
        post_id=1,
        text='Nice!',
        is_published=True,
        created_at='2024-01-01T00:00:00',
        author=make_comment_author(),
    )


class TestGetAllComments:
    @pytest.mark.asyncio
    async def test_get_all_empty(
        self, async_client: AsyncClient, override_use_case
    ):
        override_use_case(
            get_get_all_comments_use_case, lambda *args, **kwargs: []
        )
        response = await async_client.get('/comments')
        assert response.status_code == 200
        assert response.json() == []


class TestGetCommentById:
    @pytest.mark.asyncio
    async def test_get_by_id_success(
        self, async_client: AsyncClient, override_use_case
    ):
        override_use_case(
            get_get_comment_by_id_use_case,
            lambda *args, **kwargs: make_comment(),
        )
        response = await async_client.get('/comment/1')
        assert response.status_code == 200
        assert response.json()['text'] == 'Nice!'

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self, async_client: AsyncClient, override_use_case
    ):
        async def mock_get(*args, **kwargs):
            raise CommentNotFoundByIdException(id=999)

        override_use_case(get_get_comment_by_id_use_case, mock_get)
        response = await async_client.get('/comment/999')
        assert response.status_code == 404


class TestCreateComment:
    @pytest.mark.asyncio
    async def test_create_success(
        self, async_client: AsyncClient, override_auth, override_use_case
    ):
        override_use_case(
            get_create_comment_use_case, lambda *args, **kwargs: make_comment()
        )
        response = await async_client.post(
            '/comment',
            json={'post_id': 1, 'text': 'Great post!'},
        )
        assert response.status_code == 201

    @pytest.mark.asyncio
    async def test_create_post_not_found(
        self, async_client: AsyncClient, override_auth, override_use_case
    ):
        async def mock_create(*args, **kwargs):
            raise PostNotFoundByIdException(id=999)

        override_use_case(get_create_comment_use_case, mock_create)
        response = await async_client.post(
            '/comment', json={'post_id': 999, 'text': 'Nope'}
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_create_unauthorized(self, async_client: AsyncClient):
        response = await async_client.post(
            '/comment', json={'post_id': 1, 'text': 'Hack'}
        )
        assert response.status_code == 401


class TestUpdateComment:
    @pytest.mark.asyncio
    async def test_update_success(
        self, async_client: AsyncClient, override_auth, override_use_case
    ):
        async def mock_update(*args, **kwargs):
            return make_comment()

        override_use_case(get_update_comment_use_case, mock_update)
        response = await async_client.put(
            '/comment/1', json={'text': 'Updated!'}
        )
        assert response.status_code == 200
        assert response.json()['text'] == 'Nice!'

    @pytest.mark.asyncio
    async def test_update_forbidden(
        self, async_client: AsyncClient, override_auth, override_use_case
    ):
        async def mock_update(*args, **kwargs):
            raise ForbiddenActionException()

        override_use_case(get_update_comment_use_case, mock_update)
        response = await async_client.put('/comment/1', json={'text': 'Hack'})
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_update_not_found(
        self, async_client: AsyncClient, override_auth, override_use_case
    ):
        async def mock_update(*args, **kwargs):
            raise CommentNotFoundByIdException(id=999)

        override_use_case(get_update_comment_use_case, mock_update)
        response = await async_client.put(
            '/comment/999', json={'text': 'Nope'}
        )
        assert response.status_code == 404


class TestDeleteComment:
    @pytest.mark.asyncio
    async def test_delete_success(
        self, async_client: AsyncClient, override_auth, override_use_case
    ):
        override_use_case(
            get_delete_comment_use_case, lambda *args, **kwargs: None
        )
        response = await async_client.delete('/comment/1')
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_delete_forbidden(
        self, async_client: AsyncClient, override_auth, override_use_case
    ):
        async def mock_delete(*args, **kwargs):
            raise ForbiddenActionException()

        override_use_case(get_delete_comment_use_case, mock_delete)
        response = await async_client.delete('/comment/1')
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_delete_not_found(
        self, async_client: AsyncClient, override_auth, override_use_case
    ):
        async def mock_delete(*args, **kwargs):
            raise CommentNotFoundByIdException(id=999)

        override_use_case(get_delete_comment_use_case, mock_delete)
        response = await async_client.delete('/comment/999')
        assert response.status_code == 404
