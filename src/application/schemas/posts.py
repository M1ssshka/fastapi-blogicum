from pydantic import Field, ConfigDict
from datetime import datetime

from application.schemas.base import BaseCreatedAtSchema, BasePublishedSchema
from application.schemas.users import UserSchema
from application.schemas.categories import CategorySchema
from application.schemas.locations import LocationSchema


class PostCreateSchema(BasePublishedSchema):
    model_config = ConfigDict(from_attributes=True)

    title: str = Field(
        ..., min_length=1, max_length=256, description='Заголовок'
    )
    text: str = Field(..., min_length=1, description='Текст')
    pub_date: datetime = Field(..., description='Дата и время публикации')
    location_id: int | None = Field(None, description='ID местоположения')
    category_id: int | None = Field(None, description='ID категории')
    image: str | None = Field(
        None, max_length=512, description='Путь к изображению'
    )


class PostUpdateSchema(BasePublishedSchema):
    model_config = ConfigDict(from_attributes=True)

    title: str = Field(
        ..., min_length=1, max_length=256, description='Заголовок'
    )
    text: str = Field(..., min_length=1, description='Текст')
    location_id: int | None = Field(None, description='ID местоположения')
    category_id: int | None = Field(None, description='ID категории')


class PostResponseSchema(BasePublishedSchema, BaseCreatedAtSchema):
    model_config = ConfigDict(from_attributes=True)

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
    category: CategorySchema | None = Field(None, description='Категория')
    image: str | None = Field(None, description='Путь к изображению')
