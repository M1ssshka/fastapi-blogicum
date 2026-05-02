from typing import Type, TypeVar, Generic, Any

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from application.infrastructure.database.database import Base

ModelType = TypeVar('ModelType', bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(
        self,
        model: Type[ModelType],
        not_found_exception_class: Type[Exception],
    ):
        self._model = model
        self._not_found_exception_class = not_found_exception_class

    async def create(self, session: AsyncSession, **data) -> ModelType:
        query = insert(self._model).values(**data).returning(self._model)
        obj = await session.scalar(query)
        return obj

    async def get_by_id(self, session: AsyncSession, id: int) -> ModelType:
        query = select(self._model).where(self._model.id == id)
        obj = await session.scalar(query)
        if obj is None:
            raise self._not_found_exception_class()
        return obj

    async def get_all(
        self,
        session: AsyncSession,
        limit: int = 100,
        offset: int = 0,
        options: list[Any] | None = None,
    ) -> list[ModelType]:
        query = select(self._model)
        if options:
            query = query.options(*options)
        query = query.limit(limit).offset(offset)
        result = await session.execute(query)
        return list(result.scalars().all())

    async def update(
        self, session: AsyncSession, id: int, **data
    ) -> ModelType:
        obj = await self.get_by_id(session, id)
        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        return obj

    async def delete(self, session: AsyncSession, id: int) -> None:
        obj = await self.get_by_id(session, id)
        await session.delete(obj)
