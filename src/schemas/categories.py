from pydantic import Field, ConfigDict
from schemas.base import BasePublishedSchema, BaseCreatedAtSchema


class CategorySchema(BasePublishedSchema, BaseCreatedAtSchema):
    model_config = ConfigDict(from_attributes=True)

    title: str = Field(..., max_length=256, description='Заголовок')
    description: str = Field(..., description='Описание')
    slug: str = Field(
        ...,
        pattern=r'^[a-zA-Z0-9_-]+$',
        description='Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание.',
    )
