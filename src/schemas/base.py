from pydantic import BaseModel, Field
from datetime import datetime


class BasePublished(BaseModel):
    is_published: bool = Field(
        True,
        title='Опубликовано',
    )


class BaseCreatedAt(BaseModel):
    created_at: datetime = Field(title='Добавлено')
