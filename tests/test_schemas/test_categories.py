import pytest
from pydantic import ValidationError
from application.schemas.categories import CategoryCreateSchema
from datetime import datetime


class TestCategoryCreateSchema:
    def test_valid(self):
        data = CategoryCreateSchema(
            title='Tech',
            description='Tech category',
            slug='tech',
            created_at=datetime(2024, 1, 1),
        )
        assert data.slug == 'tech'

    def test_invalid_slug_raises(self):
        with pytest.raises(ValidationError):
            CategoryCreateSchema(
                title='Tech',
                description='Desc',
                slug='tech slug',
                created_at=datetime(2024, 1, 1),
            )
