from datetime import datetime

from pydantic import BaseModel, SecretStr, ConfigDict


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    password: SecretStr
    first_name: str
    last_name: str
    email: str
    is_staff: bool
    is_active: bool
    is_superuser: bool
    date_joined: datetime
    last_login: datetime | None = None
