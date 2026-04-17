from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from infrastructure.sqlite.repositories.base import BaseRepository
from infrastructure.sqlite.models.categories import Category

from core.exceptions.database_exceptions import (
    CategorySlugConflictException,
    CategoryNotFoundException,
)


class CategoryRepository(BaseRepository[Category]):
    def __init__(self):
        super().__init__(Category, CategoryNotFoundException)

    def get_by_slug(self, session: Session, slug: str) -> Category:
        query = session.query(self._model).where(self._model.slug == slug)
        category = query.scalar()
        if not category:
            raise CategoryNotFoundException(slug)
        return category

    def create(self, session: Session, **kwargs) -> Category:
        try:
            return super().create(session=session, **kwargs)
        except IntegrityError:
            raise CategorySlugConflictException()
