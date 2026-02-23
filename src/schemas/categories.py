from pydantic import Field
from src.schemas.base import BasePublishedSchema, BaseCreatedAtSchema


class CategorySchema(BasePublishedSchema, BaseCreatedAtSchema):
    title: str = Field(..., max_length=256, description='Заголовок')
    description: str = Field(..., description='Описание')
    slug: str = Field(
        ...,
        pattern=r'^[a-zA-Z0-9_-]+$',
        description='Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание.',
    )
