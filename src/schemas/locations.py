from pydantic import Field, ConfigDict
from schemas.base import BaseCreatedAtSchema, BasePublishedSchema


class LocationSchema(BasePublishedSchema, BaseCreatedAtSchema):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., description='Название места', max_length=256)
