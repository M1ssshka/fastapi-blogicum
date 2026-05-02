from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from application.infrastructure.database.repositories.base import (
    BaseRepository,
)
from application.infrastructure.database.models.locations import Location
from application.core.exceptions.database_exceptions import (
    LocationNameConflictException,
    LocationNotFoundException,
)


class LocationRepository(BaseRepository[Location]):
    def __init__(self):
        super().__init__(Location, LocationNotFoundException)

    async def create(self, session: AsyncSession, **kwargs) -> Location:
        try:
            return await super().create(session=session, **kwargs)
        except IntegrityError:
            raise LocationNameConflictException()
