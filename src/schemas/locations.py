from pydantic import Field
from src.schemas.base import BaseCreatedAt, BasePublished


class Location(BasePublished, BaseCreatedAt):
    name: str = Field(..., title='Название места', max_length=256)
