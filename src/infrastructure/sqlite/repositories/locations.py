from typing import Type

from sqlalchemy.orm import Session

from infrastructure.sqlite.models.locations import Location


class LocationRepository:
    def __init__(self):
        self._model: Type[Location] = Location

    def get(self, session: Session, location_id: int) -> Location | None:
        query = session.query(self._model).where(self._model.id == location_id)
        return query.scalar()
