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
        await assert_get_all_empty(
            async_client,
            override_use_case,
            get_get_all_comments_use_case,
            '/comments',
        )

    @pytest.mark.asyncio
    async def test_get_all_with_data(
        self, async_client: AsyncClient, override_use_case
    ):
        await assert_get_all_with_data(
            async_client,
            override_use_case,
            get_get_all_comments_use_case,
            '/comments',
            make_comment,
        )


class TestGetCommentById:
    @pytest.mark.asyncio
    async def test_get_by_id_success(
        self, async_client: AsyncClient, override_use_case
    ):
        await assert_get_by_id_success(
            async_client,
            override_use_case,
            get_get_comment_by_id_use_case,
            '/comment/1',
            make_comment,
        )

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self, async_client: AsyncClient, override_use_case
    ):
        await assert_get_by_id_not_found(
            async_client,
            override_use_case,
            get_get_comment_by_id_use_case,
            '/comment/999',
            CommentNotFoundByIdException,
        )


class TestCreateComment:
    @pytest.mark.asyncio
    async def test_create_success(
        self, async_client: AsyncClient, override_auth, override_use_case
    ):
        await assert_create_success(
            async_client,
            override_use_case,
            get_create_comment_use_case,
            '/comment',
            {'post_id': 1, 'text': 'Great post!'},
            make_comment,
        )

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
        await assert_create_unauthorized(
            async_client, '/comment', {'post_id': 1, 'text': 'Hack'}
        )


class TestUpdateComment:
    @pytest.mark.asyncio
    async def test_update_success(
        self, async_client: AsyncClient, override_auth, override_use_case
    ):
        await assert_update_success(
            async_client,
            override_use_case,
            get_update_comment_use_case,
            '/comment/1',
            {'text': 'Updated!'},
            make_comment,
        )

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
        await assert_update_not_found(
            async_client,
            override_use_case,
            get_update_comment_use_case,
            '/comment/999',
            {'text': 'Nope'},
            CommentNotFoundByIdException,
        )


class TestDeleteComment:
    @pytest.mark.asyncio
    async def test_delete_success(
        self, async_client: AsyncClient, override_auth, override_use_case
    ):
        await assert_delete_success(
            async_client,
            override_use_case,
            get_delete_comment_use_case,
            '/comment/1',
        )

    @pytest.mark.asyncio
    async def test_delete_forbidden(
        self, async_client: AsyncClient, override_auth, override_use_case
    ):
        await assert_delete_forbidden(
            async_client,
            override_use_case,
            get_delete_comment_use_case,
            '/comment/1',
        )

    @pytest.mark.asyncio
    async def test_delete_not_found(
        self, async_client: AsyncClient, override_auth, override_use_case
    ):
        await assert_delete_not_found(
            async_client,
            override_use_case,
            get_delete_comment_use_case,
            '/comment/999',
            CommentNotFoundByIdException,
        )
