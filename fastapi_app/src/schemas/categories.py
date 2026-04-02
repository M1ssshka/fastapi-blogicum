from pydantic import Field, ConfigDict, BaseModel
from schemas.base import BasePublishedSchema, BaseCreatedAtSchema


class CategoryCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str = Field(..., max_length=256, description='Заголовок')
    description: str = Field(..., description='Описание')
    slug: str = Field(
        ...,
        pattern=r'^[a-zA-Z0-9_-]+$',
        description='Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание.',
    )
    is_published: bool = Field(True, description='Опубликовано')


class CategoryUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str = Field(..., max_length=256, description='Заголовок')
    description: str = Field(..., description='Описание')
    is_published: bool = Field(True, description='Опубликовано')


class CategorySchema(BasePublishedSchema, BaseCreatedAtSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description='ID')
    title: str = Field(..., max_length=256, description='Заголовок')
    description: str = Field(..., description='Описание')
    slug: str = Field(
        ...,
        pattern=r'^[a-zA-Z0-9_-]+$',
        description='Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание.',
    )
