from typing import List

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.locations import LocationRepository
from schemas.locations import LocationSchema


class GetAllLocationsUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, limit: int = 100, offset: int = 0) -> List[LocationSchema]:
        with self._database.session() as session:
            locations = self._repo.get_all(session=session, limit=limit, offset=offset)

        return [LocationSchema.model_validate(obj=loc) for loc in locations]
