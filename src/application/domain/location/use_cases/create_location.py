import logging
from datetime import datetime, timezone

from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.locations import LocationRepository
from application.schemas.locations import LocationSchema, LocationCreateSchema
from application.core.exceptions.database_exceptions import LocationNameConflictException
from application.core.exceptions.domain_exceptions import (
    LocationNameAlreadyExistsException,
    ForbiddenActionException,
)

logger = logging.getLogger(__name__)


class CreateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(
        self, dto: LocationCreateSchema, is_superuser: bool = False
    ) -> LocationSchema:
        if not is_superuser:
            error = ForbiddenActionException()
            logger.error('Попытка создать локацию без прав суперпользователя')
            raise error

        async with self._database.session() as session:
            try:
                location = await self._repo.create(
                    session=session,
                    name=dto.name,
                    is_published=dto.is_published,
                    created_at=datetime.now(timezone.utc).replace(tzinfo=None),
                )
            except LocationNameConflictException:
                raise LocationNameAlreadyExistsException(dto.name)

        return LocationSchema.model_validate(obj=location)
