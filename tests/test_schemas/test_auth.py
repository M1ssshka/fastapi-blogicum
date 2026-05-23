import pytest
from pydantic import ValidationError, Field
from pydantic import BaseModel

from application.schemas.auth import Token, RefreshTokenRequest


class TestToken:
    def test_valid_token(self):
        token = Token(
            access_token='eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0In0.test',
            refresh_token='abc123',
            token_type='bearer',
        )
        assert token.access_token.startswith('eyJ')
        assert token.refresh_token == 'abc123'
        assert token.token_type == 'bearer'

    def test_token_type_default_not_needed(self):
        t = Token(access_token='a', refresh_token='b', token_type='bearer')
        assert t.token_type == 'bearer'

    def test_empty_access_token_allowed(self):
        t = Token(access_token='', refresh_token='b', token_type='bearer')
        assert t.access_token == ''


class TestRefreshTokenRequest:
    def test_valid_request(self):
        req = RefreshTokenRequest(refresh_token='some-refresh-token')
        assert req.refresh_token == 'some-refresh-token'

    def test_empty_token_allowed(self):
        req = RefreshTokenRequest(refresh_token='')
        assert req.refresh_token == ''
