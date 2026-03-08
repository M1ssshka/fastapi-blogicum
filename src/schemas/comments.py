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

    text: str = Field(..., description='Текст комментария')


class CommentCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    post_id: int = Field(..., description='Публикация')
    author: UserSchema = Field(..., description='Автор комментария')
    text: str = Field(..., description='Текст комментария')
