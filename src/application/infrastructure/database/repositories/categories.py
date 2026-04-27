from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from application.infrastructure.database.repositories.base import BaseRepository
from application.infrastructure.database.models.categories import Category
from application.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
    CategoryNotFoundBySlugException,
)
from application.core.exceptions.database_exceptions import CategorySlugConflictException


class CategoryRepository(BaseRepository[Category]):
    def __init__(self):
        super().__init__(Category, CategoryNotFoundByIdException)

    def get_by_slug(self, session: Session, slug: str) -> Category:
        query = session.query(self._model).where(self._model.slug == slug)
        category = query.scalar()
        if not category:
            raise CategoryNotFoundBySlugException(slug)
        return category

    def create(self, session: Session, **kwargs) -> Category:
        try:
            return super().create(session=session, **kwargs)
        except IntegrityError:
            raise CategorySlugConflictException()
