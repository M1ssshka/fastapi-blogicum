import pytest
from pydantic import ValidationError
from application.schemas.users import (
    UserCreateSchema,
    UserUpdateSchema,
    UserSchema,
    UserResponseSchema,
)
from datetime import datetime


class TestUserCreateSchema:
    def test_valid(self):
        data = UserCreateSchema(
            username='testuser',
            password='strongpass123',
            email='test@example.com',
            first_name='John',
            last_name='Doe',
        )
        assert data.username == 'testuser'

    def test_short_password_raises(self):
        with pytest.raises(ValidationError):
            UserCreateSchema(
                username='testuser',
                password='short',
            )

    def test_invalid_username_raises(self):
        with pytest.raises(ValidationError):
            UserCreateSchema(
                username='test user',
                password='strongpass123',
            )


class TestUserUpdateSchema:
    def test_empty_update(self):
        data = UserUpdateSchema()
        assert data.model_dump(exclude_unset=True) == {}

    def test_partial_update(self):
        data = UserUpdateSchema(first_name='NewName')
        assert data.first_name == 'NewName'
        assert data.password is None


class TestUserSchema:
    def test_from_attributes(self):
        dt = datetime(2024, 1, 1)
        user = UserSchema(
            id=1,
            username='test',
            password='hashed',
            first_name='John',
            last_name='Doe',
            email='test@example.com',
            is_staff=False,
            is_active=True,
            is_superuser=False,
            date_joined=dt,
            last_login=None,
        )
        assert user.id == 1
        assert user.username == 'test'


class TestUserResponseSchema:
    def test_response(self):
        dt = datetime(2024, 1, 1)
        resp = UserResponseSchema(
            id=1,
            username='test',
            first_name='John',
            last_name='Doe',
            email='test@example.com',
            is_active=True,
            date_joined=dt,
        )
        assert resp.model_dump(exclude_unset=True) == {
            'id': 1,
            'username': 'test',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'test@example.com',
            'is_active': True,
            'date_joined': dt,
        }
