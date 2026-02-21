from pydantic import Field
from src.schemas.base import BasePublished, BaseCreatedAt


class Category(BasePublished, BaseCreatedAt):
    title: str = Field(..., max_length=256, title='Заголовок')
    description: str = Field(..., title='Описание')
    slug: str = Field(
        ...,
        title='Идентификатор',
        pattern=r'^[a-zA-Z0-9_-]+$',
        description='Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание.',
    )
