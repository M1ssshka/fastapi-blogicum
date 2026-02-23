from pydantic import Field
from datetime import datetime
# from fastapi import UploadFile, File

from src.schemas.locations import LocationSchema
from src.schemas.categories import CategorySchema
from src.schemas.base import BaseCreatedAtSchema, BasePublishedSchema
from src.schemas.users import UserSchema


class PostCreateSchema(BasePublishedSchema):
    title: str = Field(..., max_length=256, description='Заголовок')
    text: str = Field(..., description='Текст')
    pub_date: datetime = Field(..., description='Дата и время публикации')
    author: UserSchema = Field(..., description='Автор публикации')
    location: LocationSchema | None = Field(None, description='Местоположение')
    category: CategorySchema | None = Field(..., description='Категория')
    # image: UploadFile | None = File(None, title='Фото')


class PostUpdateSchema(BasePublishedSchema):
    title: str = Field(..., max_length=256, description='Заголовок')
    text: str = Field(..., description='Текст')
    location: LocationSchema | None = Field(None, description='Местоположение')
    category: CategorySchema | None = Field(..., description='Категория')


class PostResponseSchema(BasePublishedSchema, BaseCreatedAtSchema):
    id: int = Field(..., description='ID')
    title: str = Field(..., max_length=256, description='Заголовок')
    text: str = Field(..., description='Текст')
    pub_date: datetime = Field(
        ...,
        title='Дата и время публикации',
        description='Если установить дату и время в будущем — можно делать отложенные публикации.',
    )
    author: UserSchema = Field(..., description='Автор публикации')
    location: LocationSchema | None = Field(None, description='Местоположение')
    category: CategorySchema | None = Field(..., description='Категория')
    # image: str | None = Field(None, title='Путь к изображению')
