import pytest
from pydantic import ValidationError
from application.schemas.locations import LocationCreateSchema


class TestLocationCreateSchema:
    def test_valid(self):
        data = LocationCreateSchema(name='Moscow')
        assert data.name == 'Moscow'
        assert data.is_published is True

    def test_empty_name_raises(self):
        with pytest.raises(ValidationError):
            LocationCreateSchema(name='')


class TestLocationSchema:
    pass
