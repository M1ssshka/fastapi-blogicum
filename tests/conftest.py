import asyncio
from collections.abc import AsyncGenerator
from unittest.mock import patch

import pytest
from pytest import FixtureRequest

from tests.mocks import FakeDatabase, FakeSession

# Prevent real DB engine creation during import
_patcher = patch('application.infrastructure.database.database.Database')
_patcher.start()

from application.infrastructure.database.database import database


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def fake_session() -> FakeSession:
    return FakeSession()


@pytest.fixture
def fake_db(fake_session: FakeSession) -> FakeSession:
    db = FakeDatabase(fake_session)
    with patch.object(database, 'session', db.session):
        yield fake_session
