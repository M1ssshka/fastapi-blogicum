from pydantic import Field, ConfigDict, BaseModel
from schemas.base import BaseCreatedAtSchema, BasePublishedSchema


class LocationCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(
        ..., min_length=1, max_length=256, description='Название места'
    )
    is_published: bool = Field(True, description='Опубликовано')


class LocationUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(
        ..., min_length=1, max_length=256, description='Название места'
    )
    is_published: bool = Field(True, description='Опубликовано')


class LocationSchema(BasePublishedSchema, BaseCreatedAtSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description='ID')
    name: str = Field(..., description='Название места', max_length=256)
