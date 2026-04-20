from datetime import datetime

from pydantic import BaseModel, SecretStr, ConfigDict, Field
from schemas.base import UsernameStr, ValidatedEmail


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: UsernameStr
    password: SecretStr
    first_name: str = Field(..., min_length=1, max_length=150, description='Имя')
    last_name: str = Field(..., min_length=1, max_length=150, description='Фамилия')
    email: ValidatedEmail
    is_staff: bool
    is_active: bool
    is_superuser: bool
    date_joined: datetime
    last_login: datetime | None = None
