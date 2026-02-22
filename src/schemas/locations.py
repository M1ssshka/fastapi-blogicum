from pydantic import Field
from src.schemas.base import BaseCreatedAtSchema, BasePublishedSchema


class LocationSchema(BasePublishedSchema, BaseCreatedAtSchema):
    name: str = Field(..., title='Название места', max_length=256)
