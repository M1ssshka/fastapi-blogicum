from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.locations import LocationRepository
from core.exceptions.domain_exceptions import ForbiddenActionException


class DeleteLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int, is_superuser: bool = False) -> bool:
        if not is_superuser:
            raise ForbiddenActionException()
        
        with self._database.session() as session:
            self._repo.delete(session=session, id=location_id)

        return True
