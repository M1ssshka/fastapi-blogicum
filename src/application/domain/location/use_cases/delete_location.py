import logging

from application.core.exceptions.database_exceptions import (
    LocationNotFoundException,
)
from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.locations import (
    LocationRepository,
)
from application.core.exceptions.domain_exceptions import (
    ForbiddenActionException,
    LocationNotFoundByIdException,
)

logger = logging.getLogger(__name__)


class DeleteLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(
        self, location_id: int, is_superuser: bool = False
    ) -> bool:
        if not is_superuser:
            error = ForbiddenActionException()
            logger.error(
                f'Попытка удалить локацию {location_id} без прав суперпользователя'
            )
            raise error
        try:
            async with self._database.session() as session:
                await self._repo.delete(session=session, id=location_id)
        except LocationNotFoundException:
            logger.error(f'Локация с id: {location_id} не найдена для удаления')
            raise LocationNotFoundByIdException(id=location_id)
        return True
