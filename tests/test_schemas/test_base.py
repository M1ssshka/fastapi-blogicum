import pytest
from pydantic import BaseModel, Field, ValidationError, create_model
from typing import Annotated

from application.schemas.base import (
    SlugStr,
    UsernameStr,
    NameStr,
    ValidatedEmail,
    validate_slug,
    validate_username,
    validate_name,
)


class TestSlugValidation:
    def test_valid_slugs(self):
        for slug in ['hello-world', 'test_slug', 'slug123', 'a', 'a-b_c']:
            assert validate_slug(slug) == slug

    def test_invalid_slugs(self):
        for slug in ['русский', 'slug with spaces', 'slug!']:
            with pytest.raises(
                ValueError, match='Slug может содержать только'
            ):
                validate_slug(slug)


class TestUsernameValidation:
    def test_valid_usernames(self):
        for name in ['john_doe', 'user123', 'a', 'abc']:
            assert validate_username(name) == name

    def test_invalid_usernames(self):
        for name in ['user name', 'user-name', 'привет']:
            with pytest.raises(
                ValueError, match='Username может содержать только'
            ):
                validate_username(name)


class TestNameValidation:
    def test_valid_names(self):
        for name in ['John', 'Анна', 'O', 'Marie-Anne']:
            assert validate_name(name) == name

    def test_invalid_names(self):
        for name in ['', '  ', 'John123']:
            with pytest.raises(ValueError):
                validate_name(name)


SlugModel = create_model('SlugModel', slug=(SlugStr, ...))
UsernameModel = create_model('UsernameModel', username=(UsernameStr, ...))
NameModel = create_model('NameModel', name=(NameStr, ...))
EmailModel = create_model('EmailModel', email=(ValidatedEmail, ...))


class TestSlugStrField:
    def test_valid_slug(self):
        model = SlugModel(slug='hello-world')
        assert model.slug == 'hello-world'

    def test_invalid_slug(self):
        with pytest.raises(ValidationError):
            SlugModel(slug='плохой slug')

    def test_empty_slug_raises(self):
        with pytest.raises(ValidationError):
            SlugModel(slug='')


class TestUsernameStrField:
    def test_valid(self):
        model = UsernameModel(username='john_doe')
        assert model.username == 'john_doe'

    def test_invalid(self):
        with pytest.raises(ValidationError):
            UsernameModel(username='user name')

    def test_too_short(self):
        with pytest.raises(ValidationError):
            UsernameModel(username='ab')


class TestNameStrField:
    def test_valid(self):
        model = NameModel(name='John')
        assert model.name == 'John'

    def test_invalid(self):
        with pytest.raises(ValidationError):
            NameModel(name='User123')


class TestValidatedEmailField:
    def test_valid_emails(self):
        model = EmailModel(email='user@example.com')
        assert model.email == 'user@example.com'

    def test_valid_none(self):
        model = EmailModel(email=None)
        assert model.email is None

    def test_invalid_emails(self):
        with pytest.raises(ValidationError):
            EmailModel(email='not-an-email')
