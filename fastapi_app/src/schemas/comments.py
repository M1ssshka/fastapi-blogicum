from pydantic import Field, BaseModel, ConfigDict

from schemas.base import BaseCreatedAtSchema, BasePublishedSchema
from schemas.users import UserSchema


class CommentResponse(BasePublishedSchema, BaseCreatedAtSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description='ID')
    post_id: int = Field(..., description='Публикация')
    author: UserSchema = Field(..., description='Автор комментария')
    text: str = Field(..., description='Текст комментария')


class CommentUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    text: str = Field(..., min_length=1, max_length=1000, description='Текст комментария')


class CommentCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    post_id: int = Field(..., description='Публикация')
    author_id: int = Field(..., description='ID автора комментария')
    text: str = Field(..., min_length=1, max_length=1000, description='Текст комментария')
    is_published: bool = Field(True, description='Опубликовано')
