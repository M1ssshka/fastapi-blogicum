from typing import Type, TypeVar, Generic

from sqlalchemy.orm import Session
from sqlalchemy import select

from infrastructure.sqlite.database import Base

ModelType = TypeVar('ModelType', bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self._model = model

    def create(self, session: Session, **data) -> ModelType:
        obj = self._model(**data)
        session.add(obj)
        return obj

    def get_by_id(self, session: Session, id: int) -> ModelType | None:
        return session.get(self._model, id)

    def get_all(
        self, session: Session, limit: int = 100, offset: int = 0
    ) -> list[ModelType]:
        query = select(self._model).limit(limit).offset(offset)
        return list(session.scalars(query).all())

    def update(self, session: Session, id: int, **data) -> ModelType | None:
        obj = self.get_by_id(session, id)
        if obj is None:
            return None
        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        return obj

    def delete(self, session: Session, id: int) -> bool:
        obj = self.get_by_id(session, id)
        if obj is None:
            return False
        session.delete(obj)
        return True
