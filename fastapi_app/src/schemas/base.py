from pydantic import BaseModel, Field, AfterValidator, EmailStr
from datetime import datetime
from typing import Annotated
import re


class BasePublishedSchema(BaseModel):
    is_published: bool = Field(
        True,
        description='Опубликовано',
    )


class BaseCreatedAtSchema(BaseModel):
    created_at: datetime = Field(description='Добавлено')


def validate_slug(value: str) -> str:
    if not re.match(r'^[a-zA-Z0-9_-]+$', value):
        raise ValueError(
            'Slug может содержать только латинские буквы, цифры, дефис и подчёркивание'
        )
    return value


SlugStr = Annotated[
    str,
    AfterValidator(validate_slug),
    Field(
        min_length=1,
        max_length=64,
        description='Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание.',
    ),
]


def validate_username(value: str) -> str:
    if not re.match(r'^[a-zA-Z0-9_]+$', value):
        raise ValueError(
            'Username может содержать только латинские буквы, цифры и подчёркивание'
        )

    return value


UsernameStr = Annotated[
    str,
    AfterValidator(validate_username),
    Field(
        min_length=3,
        max_length=150,
        description='Имя пользователя (только латинские буквы, цифры и подчёркивание)',
    ),
]


ValidatedEmail = Annotated[
    EmailStr,
    Field(description='Email адрес'),
]
