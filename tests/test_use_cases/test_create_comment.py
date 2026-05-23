import pytest

from application.domain.comment.use_cases.create_comment import (
    CreateCommentUseCase,
)
from application.core.exceptions.domain_exceptions import (
    PostNotFoundByIdException,
)
from datetime import datetime


def make_comment_author():
    return type(
        'User',
        (),
        {
            'id': 1,
            'username': 'author',
            'password': 'hash',
            'first_name': 'A',
            'last_name': 'B',
            'email': None,
            'is_staff': False,
            'is_active': True,
            'is_superuser': False,
            'date_joined': datetime(2024, 1, 1),
            'last_login': None,
        },
    )()


def make_comment():
    return type(
        'Comment',
        (),
        {
            'id': 1,
            'text': 'Nice post!',
            'is_published': True,
            'created_at': datetime(2024, 1, 1),
            'post_id': 1,
            'author': make_comment_author(),
        },
    )()


@pytest.fixture
def use_case():
    return CreateCommentUseCase()


@pytest.mark.asyncio
async def test_create_comment_success(use_case, fake_session, fake_db):
    fake_session.scalar_results = [
        type('Post', (), {'id': 1})(),
        make_comment(),
        make_comment(),
    ]

    from application.schemas.comments import CommentCreate

    dto = CommentCreate(post_id=1, text='Nice post!')
    result = await use_case.execute(dto=dto, author_id=1)
    assert result.text == 'Nice post!'


@pytest.mark.asyncio
async def test_create_comment_post_not_found(use_case, fake_session, fake_db):
    fake_session.scalar_result = None

    from application.schemas.comments import CommentCreate

    dto = CommentCreate(post_id=999, text='Comment')

    with pytest.raises(PostNotFoundByIdException):
        await use_case.execute(dto=dto, author_id=1)
