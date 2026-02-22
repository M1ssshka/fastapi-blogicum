from pydantic import BaseModel, SecretStr


class UserSchema(BaseModel):
    username: str
    password: SecretStr
