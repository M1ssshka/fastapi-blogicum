from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.locations import LocationRepository
from schemas.locations import LocationSchema, LocationUpdateSchema


class UpdateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int, dto: LocationUpdateSchema) -> LocationSchema:
        with self._database.session() as session:
            location = self._repo.update(
                session=session,
                id=location_id,
                name=dto.name,
                is_published=dto.is_published,
            )

            if location is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Локация с id {location_id} не найдена',
                )

        return LocationSchema.model_validate(obj=location)
