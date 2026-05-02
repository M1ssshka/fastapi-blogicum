import logging

from application.core.exceptions.database_exceptions import (
    LocationNotFoundException,
)
from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.locations import (
    LocationRepository,
)
from application.schemas.locations import LocationSchema, LocationUpdateSchema
from application.core.exceptions.domain_exceptions import (
    ForbiddenActionException,
    LocationNotFoundByIdException,
)

logger = logging.getLogger(__name__)


class UpdateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(
        self,
        location_id: int,
        dto: LocationUpdateSchema,
        is_superuser: bool = False,
    ) -> LocationSchema:
        if not is_superuser:
            error = ForbiddenActionException()
            logger.error(
                f'Попытка изменить локацию {location_id} без прав суперпользователя'
            )
            raise error

        try:
            async with self._database.session() as session:
                location = await self._repo.update(
                    session=session,
                    id=location_id,
                    name=dto.name,
                    is_published=dto.is_published,
                )
        except LocationNotFoundException:
            raise LocationNotFoundByIdException(id=location_id)
        return LocationSchema.model_validate(obj=location)
