from pydantic import Field, BaseModel

from src.schemas.base import BaseCreatedAtSchema, BasePublishedSchema
from src.schemas.users import UserSchema


class CommentResponse(BasePublishedSchema, BaseCreatedAtSchema):
    post_id: int = Field(..., description='Публикация')
    author: UserSchema = Field(..., description='Автор комментария')
    text: str = Field(..., description='Текст комментария')


class CommentUpdate(BaseModel):
    text: str = Field(..., description='Текст комментария')


class CommentCreate(BaseModel):
    post_id: int = Field(..., description='Публикация')
    author: UserSchema = Field(..., description='Автор комментария')
    text: str = Field(..., description='Текст комментария')
