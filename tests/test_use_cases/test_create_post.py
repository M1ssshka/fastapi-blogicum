import pytest

from application.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
    LocationNotFoundByIdException,
)
from application.domain.post.use_cases.create_post import CreatePostUseCase
from datetime import datetime, timezone


def make_user(id=1, username='author'):
    return type(
        'User',
        (),
        {
            'id': id,
            'username': username,
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


def make_post():
    return type(
        'Post',
        (),
        {
            'id': 1,
            'title': 'Test Post',
            'text': 'Content',
            'is_published': True,
            'pub_date': datetime.now(timezone.utc),
            'created_at': datetime.now(timezone.utc),
            'image_path': None,
            'author': make_user(),
            'category': None,
            'location': None,
        },
    )()


@pytest.fixture
def use_case():
    return CreatePostUseCase()


@pytest.mark.asyncio
async def test_create_post_success(use_case, fake_session, fake_db):
    fake_session.scalar_results = [
        make_user(),  # get_by_id for category
        make_user(),  # get_by_id for location
        make_post(),  # create result
        make_post(),  # get_by_id_with_relations result
    ]

    from application.schemas.posts import PostCreateSchema

    dto = PostCreateSchema(
        title='Test Post',
        text='Content',
        pub_date=datetime.now(timezone.utc),
        category_id=1,
        location_id=1,
    )

    result = await use_case.execute(dto=dto, author_id=1)
    assert result.title == 'Test Post'


@pytest.mark.asyncio
async def test_create_post_category_not_found(use_case, fake_session, fake_db):
    fake_session.scalar_result = None

    from application.schemas.posts import PostCreateSchema
    from datetime import datetime, timezone

    dto = PostCreateSchema(
        title='Test',
        text='Content',
        pub_date=datetime.now(timezone.utc),
        category_id=999,
    )

    with pytest.raises(CategoryNotFoundByIdException):
        await use_case.execute(dto=dto, author_id=1)
