from datetime import datetime

from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.locations import LocationRepository
from schemas.locations import LocationSchema, LocationCreateSchema


class CreateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, dto: LocationCreateSchema) -> LocationSchema:
        with self._database.session() as session:
            location = self._repo.create(
                session=session,
                name=dto.name,
                is_published=dto.is_published,
                created_at=datetime.now(),
            )
            session.flush()

        return LocationSchema.model_validate(obj=location)
