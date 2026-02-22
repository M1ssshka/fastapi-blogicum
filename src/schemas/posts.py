from pydantic import Field
from datetime import datetime
# from fastapi import UploadFile, File

from src.schemas.locations import LocationSchema
from src.schemas.categories import CategorySchema
from src.schemas.base import BaseCreatedAtSchema, BasePublishedSchema
from src.schemas.users import UserSchema


class PostCreateSchema(BasePublishedSchema, BaseCreatedAtSchema):
    title: str = Field(..., max_length=256, title='Заголовок')
    text: str = Field(..., title='Текст')
    pub_date: datetime = Field(
        ...,
        title='Дата и время публикации',
        description='Если установить дату и время в будущем — можно делать отложенные публикации.',
    )
    author: UserSchema = Field(..., title='Автор публикации')
    location: LocationSchema | None = Field(None, title='Местоположение')
    category: CategorySchema | None = Field(..., title='Категория')
    # image: UploadFile | None = File(None, title='Фото')


class PostUpdateSchema(BasePublishedSchema, BaseCreatedAtSchema):
    title: str = Field(..., max_length=256, title='Заголовок')
    text: str = Field(..., title='Текст')
    pub_date: datetime = Field(
        ...,
        title='Дата и время публикации',
        description='Если установить дату и время в будущем — можно делать отложенные публикации.',
    )
    author: UserSchema = Field(..., title='Автор публикации')
    location: LocationSchema | None = Field(None, title='Местоположение')
    category: CategorySchema | None = Field(..., title='Категория')
    is_published: bool = Field(True, title='Опубликовано')


class PostResponseSchema(BasePublishedSchema, BaseCreatedAtSchema):
    id: int = Field(..., title='ID')
    title: str = Field(..., max_length=256, title='Заголовок')
    text: str = Field(..., title='Текст')
    pub_date: datetime = Field(
        ...,
        title='Дата и время публикации',
        description='Если установить дату и время в будущем — можно делать отложенные публикации.',
    )
    author: UserSchema = Field(..., title='Автор публикации')
    location: LocationSchema | None = Field(None, title='Местоположение')
    category: CategorySchema | None = Field(..., title='Категория')
    # image: str | None = Field(None, title='Путь к изображению')
