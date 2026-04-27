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

    LOG_FILE: str = 'logs/app.log'
    LOG_MAX_BYTES: int = 10485760  # 10MB
    LOG_BACKUP_COUNT: int = 5


settings = Settings()
