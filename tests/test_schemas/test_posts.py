import pytest
from pydantic import ValidationError
from application.schemas.posts import PostCreateSchema, PostUpdateSchema
from datetime import datetime, timezone


class TestPostCreateSchema:
    def test_valid(self):
        data = PostCreateSchema(
            title='Test Post',
            text='Some content here',
            pub_date=datetime.now(timezone.utc),
        )
        assert data.title == 'Test Post'
        assert data.is_published is True

    def test_invalid_title_raises(self):
        with pytest.raises(ValidationError):
            PostCreateSchema(
                title='',
                text='Content',
                pub_date=datetime.now(timezone.utc),
            )


class TestPostUpdateSchema:
    def test_empty(self):
        data = PostUpdateSchema()
        assert data.model_dump(exclude_unset=True) == {}

    def test_partial(self):
        data = PostUpdateSchema(title='New Title')
        assert data.title == 'New Title'
        assert data.text is None
