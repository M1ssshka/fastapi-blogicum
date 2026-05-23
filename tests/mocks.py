from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any, Callable


class FakeSession:
    def __init__(self) -> None:
        self.commit_calls: int = 0
        self.rollback_calls: int = 0
        self.added_objects: list[Any] = []
        self.scalar_result: Any = None
        self.scalar_results: list[Any] = []
        self.execute_result: Any = None
        self._refresh_callback: Callable[[Any], None] | None = None

    async def commit(self) -> None:
        self.commit_calls += 1

    async def rollback(self) -> None:
        self.rollback_calls += 1

    def add(self, obj: Any) -> None:
        self.added_objects.append(obj)

    async def flush(self) -> None:
        pass

    async def refresh(self, obj: Any) -> None:
        if self._refresh_callback:
            self._refresh_callback(obj)

    async def execute(self, *args: Any, **kwargs: Any) -> Any:
        return self.execute_result

    async def scalar(self, *args: Any, **kwargs: Any) -> Any:
        if self.scalar_results:
            return self.scalar_results.pop(0)
        return self.scalar_result

    async def scalars(self, *args: Any, **kwargs: Any) -> Any:
        return await self.scalar(*args, **kwargs)


class FakeDatabase:
    def __init__(self, session: FakeSession | None = None) -> None:
        self._session: FakeSession = session or FakeSession()

    @asynccontextmanager
    async def session(self) -> AsyncIterator[FakeSession]:
        yield self._session
