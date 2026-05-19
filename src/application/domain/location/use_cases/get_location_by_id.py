import logging

from application.core.exceptions.database_exceptions import (
    LocationNotFoundException,
)
from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.locations import (
    LocationRepository,
)
from application.core.exceptions.domain_exceptions import (
    LocationNotFoundByIdException,
)
from application.schemas.locations import LocationSchema

logger = logging.getLogger(__name__)


class GetLocationByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> LocationSchema:
        try:
            async with self._database.session() as session:
                location = await self._repo.get_by_id(
                    session=session, id=location_id
                )
        except LocationNotFoundException:
            logger.error(f'Локация с id: {location_id} не найдена')
            raise LocationNotFoundByIdException(id=location_id)
        return LocationSchema.model_validate(obj=location)
