import logging

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.locations import LocationRepository
from schemas.locations import LocationSchema, LocationUpdateSchema
from core.exceptions.domain_exceptions import ForbiddenActionException

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

        with self._database.session() as session:
            location = self._repo.update(
                session=session,
                id=location_id,
                name=dto.name,
                is_published=dto.is_published,
            )

        return LocationSchema.model_validate(obj=location)
