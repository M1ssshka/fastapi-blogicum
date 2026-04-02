from pydantic import Field, ConfigDict, BaseModel
from schemas.base import BaseCreatedAtSchema, BasePublishedSchema


class LocationCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., description='Название места', max_length=256)
    is_published: bool = Field(True, description='Опубликовано')


class LocationUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., description='Название места', max_length=256)
    is_published: bool = Field(True, description='Опубликовано')


class LocationSchema(BasePublishedSchema, BaseCreatedAtSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description='ID')
    name: str = Field(..., description='Название места', max_length=256)
