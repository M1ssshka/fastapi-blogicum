from typing import Type

from sqlalchemy.orm import Session

from infrastructure.sqlite.models.categories import Category


class CategoryRepository:
    def __init__(self):
        self._model: Type[Category] = Category

    def get(self, session: Session, slug: str) -> Category | None:
        query = session.query(self._model).where(self._model.slug == slug)

        return query.scalar()
