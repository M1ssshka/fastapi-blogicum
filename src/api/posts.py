from datetime import datetime
from fastapi import APIRouter
from pydantic.types import SecretStr
from src.schemas.posts import Post
from src.schemas.users import User

router = APIRouter()


@router.get('/posts')
def get_posts() -> Post:
    return Post(
        created_at=datetime.now(),
        is_published=True,
        title='string',
        text='string',
        pub_date=datetime.now(),
        author=User(username='string', password=SecretStr('string')),
        location=None,
        category=None,
    )
