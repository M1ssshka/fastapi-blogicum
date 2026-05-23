import pytest
from pydantic import ValidationError
from application.schemas.comments import CommentCreate, CommentUpdate


class TestCommentCreate:
    def test_valid(self):
        data = CommentCreate(post_id=1, text='Nice post!')
        assert data.post_id == 1
        assert data.text == 'Nice post!'
        assert data.is_published is True

    def test_empty_text_raises(self):
        with pytest.raises(ValidationError):
            CommentCreate(post_id=1, text='')


class TestCommentUpdate:
    def test_valid(self):
        data = CommentUpdate(text='Updated')
        assert data.text == 'Updated'
