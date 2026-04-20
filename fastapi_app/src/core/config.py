from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    ORIGINS: str
    PORT: int = 8000
    ROOT_PATH: str = ''

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5
    SECRET_AUTH_KEY: SecretStr
    AUTH_ALGORITHM: str = 'HS256'

    SQLITE_URL: str


settings = Settings()
