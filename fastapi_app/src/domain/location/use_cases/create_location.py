from datetime import datetime

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.locations import LocationRepository
from schemas.locations import LocationSchema, LocationCreateSchema
from core.exceptions.database_exceptions import LocationNameConflictException
from core.exceptions.domain_exceptions import LocationNameAlreadyExistsException, ForbiddenActionException


class CreateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, dto: LocationCreateSchema, is_superuser: bool = False) -> LocationSchema:
        if not is_superuser:
            raise ForbiddenActionException()
        
        with self._database.session() as session:
            try:
                location = self._repo.create(
                    session=session,
                    name=dto.name,
                    is_published=dto.is_published,
                    created_at=datetime.now(),
                )
            except LocationNameConflictException:
                raise LocationNameAlreadyExistsException(dto.name)

        return LocationSchema.model_validate(obj=location)
