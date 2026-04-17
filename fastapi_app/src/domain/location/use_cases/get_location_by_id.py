from core.exceptions.database_exceptions import LocationNotFoundException
from core.exceptions.domain_exceptions import LocationNotFoundByIdException
from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.locations import LocationRepository
from schemas.locations import LocationSchema


class GetLocationByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> LocationSchema:
        try:
            with self._database.session() as session:
                location = self._repo.get_by_id(
                    session=session, id=location_id
                )
        except LocationNotFoundException:
            raise LocationNotFoundByIdException(location_id)
        return LocationSchema.model_validate(obj=location)
