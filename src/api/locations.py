from datetime import datetime
from fastapi import APIRouter, status, HTTPException, Depends
from schemas.locations import LocationSchema

from domain.location.use_cases.get_location_by_id import GetLocationByIdUseCase
from api.depends import (
    get_get_location_by_id_use_case,
)

router = APIRouter()


@router.get(
    '/location/{location_id}',
    status_code=status.HTTP_200_OK,
    response_model=LocationSchema,
)
async def get_location_by_id(
    location_id: int,
    use_case: GetLocationByIdUseCase = Depends(
        get_get_location_by_id_use_case
    ),
) -> LocationSchema:
    location = await use_case.execute(location_id=location_id)

    return location
