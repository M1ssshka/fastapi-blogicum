from datetime import datetime

from pydantic import BaseModel, SecretStr, ConfigDict, Field
from application.schemas.base import UsernameStr, ValidatedEmail, NameStr


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: UsernameStr
    password: SecretStr
    first_name: NameStr
    last_name: NameStr
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
    first_name: NameStr = Field('', description='Имя')
    last_name: NameStr = Field('', description='Фамилия')


class UserUpdateSchema(BaseModel):
    username: UsernameStr | None = Field(None, description='Имя пользователя')
    password: str | None = Field(
        None, min_length=8, max_length=128, description='Пароль'
    )
    email: ValidatedEmail | None = Field(None, description='Email')
    first_name: NameStr | None = Field(None, description='Имя')
    last_name: NameStr | None = Field(None, description='Фамилия')
    is_active: bool | None = Field(None, description='Активен')
    is_staff: bool | None = Field(None, description='Стафф')
    is_superuser: bool | None = Field(None, description='Суперюзер')


class UserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: UsernameStr
    first_name: NameStr
    last_name: NameStr
    email: ValidatedEmail | None = None
    is_active: bool
    date_joined: datetime
