from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from application.infrastructure.database.repositories.base import BaseRepository
from application.infrastructure.database.models.locations import Location
from application.core.exceptions.domain_exceptions import LocationNotFoundByIdException
from application.core.exceptions.database_exceptions import LocationNameConflictException


class LocationRepository(BaseRepository[Location]):
    def __init__(self):
        super().__init__(Location, LocationNotFoundByIdException)

    def create(self, session: Session, **kwargs) -> Location:
        try:
            return super().create(session=session, **kwargs)
        except IntegrityError:
            raise LocationNameConflictException()
