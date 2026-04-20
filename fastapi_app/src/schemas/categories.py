from pydantic import Field, ConfigDict, BaseModel
from schemas.base import BasePublishedSchema, BaseCreatedAtSchema, SlugStr


class CategoryCreateSchema(BasePublishedSchema, BaseCreatedAtSchema):
    model_config = ConfigDict(from_attributes=True)

    title: str = Field(
        ..., min_length=1, max_length=256, description='Заголовок'
    )
    description: str = Field(
        ..., min_length=1, max_length=1000, description='Описание'
    )
    slug: SlugStr


class CategoryUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str = Field(
        ..., min_length=1, max_length=256, description='Заголовок'
    )
    description: str = Field(
        ..., min_length=1, max_length=1000, description='Описание'
    )
    is_published: bool = Field(True, description='Опубликовано')


class CategorySchema(CategoryCreateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description='ID')
    title: str = Field(..., max_length=256, description='Заголовок')
    description: str = Field(..., description='Описание')
    slug: SlugStr
