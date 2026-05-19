import logging
from typing import List

from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.locations import (
    LocationRepository,
)
from application.schemas.locations import LocationSchema

logger = logging.getLogger(__name__)


class GetAllLocationsUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(
        self, limit: int = 100, offset: int = 0
    ) -> List[LocationSchema]:
        try:
            async with self._database.session() as session:
                locations = await self._repo.get_all(
                    session=session, limit=limit, offset=offset
                )
        except Exception as e:
            logger.error(f'Ошибка при получении списка локаций: {e}')
            raise e

        return [LocationSchema.model_validate(obj=loc) for loc in locations]
