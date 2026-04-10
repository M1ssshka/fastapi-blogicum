from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.locations import LocationRepository
from schemas.locations import LocationSchema


class GetLocationByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> LocationSchema:
        with self._database.session() as session:
            location = self._repo.get_by_id(session=session, id=location_id)

        return LocationSchema.model_validate(obj=location)
