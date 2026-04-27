from datetime import datetime

from pydantic import BaseModel, SecretStr, ConfigDict, Field
from application.schemas.base import UsernameStr, ValidatedEmail


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: UsernameStr
    password: SecretStr
    first_name: str = Field(
        ..., min_length=1, max_length=150, description='Имя'
    )
    last_name: str = Field(
        ..., min_length=1, max_length=150, description='Фамилия'
    )
    email: ValidatedEmail | None = None
    is_staff: bool
    is_active: bool
    is_superuser: bool
    date_joined: datetime
    last_login: datetime | None = None


class UserCreateSchema(BaseModel):
    username: UsernameStr = Field(..., description='Имя пользователя')
    password: str = Field(
        ..., min_length=8, max_length=128, description='Пароль'
    )
    email: ValidatedEmail | None = Field(None, description='Email')
    first_name: str = Field('', max_length=150, description='Имя')
    last_name: str = Field('', max_length=150, description='Фамилия')


class UserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: UsernameStr
    first_name: str
    last_name: str
    email: ValidatedEmail | None = None
    is_active: bool
    date_joined: datetime
