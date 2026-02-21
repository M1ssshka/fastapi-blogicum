from pydantic import Field
from datetime import datetime
from fastapi import UploadFile, File

from src.schemas.users import User
from src.schemas.locations import Location
from src.schemas.categories import Category
from src.schemas.base import BaseCreatedAt, BasePublished


class Post(BasePublished, BaseCreatedAt):
    title: str = Field(..., max_length=256, title='Заголовок')
    text: str = Field(..., title='Текст')
    pub_date: datetime = Field(
        ...,
        title='Дата и время публикации',
        description='Если установить дату и время в будущем — можно делать отложенные публикации.',
    )

    author: User = Field(..., title='Автор публикации')
    location: Location | None = Field(None, title='Местоположение')
    category: Category | None = Field(..., title='Категория')
    image: UploadFile | None = File(None, title='post_images')
