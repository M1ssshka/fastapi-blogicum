from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.locations import LocationRepository
from application.schemas.locations import LocationSchema


class GetLocationByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> LocationSchema:
        async with self._database.session() as session:
            location = await self._repo.get_by_id(session=session, id=location_id)

        return LocationSchema.model_validate(obj=location)
