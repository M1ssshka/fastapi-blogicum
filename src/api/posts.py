from datetime import datetime
from fastapi import APIRouter, status, HTTPException

from src.schemas.posts import (
    PostCreateSchema,
    PostUpdateSchema,
    PostResponseSchema,
)

router = APIRouter()

fake_db = []


@router.get('/get/{post_id}')
def get_post(post_id: int):
    if post_id < len(fake_db):
        return fake_db[post_id]
    else:
        raise HTTPException(
            detail='Пост не найден',
            status_code=status.HTTP_404_NOT_FOUND,
        )


@router.post(
    '/create',
    status_code=status.HTTP_201_CREATED,
    response_model=PostResponseSchema,
)
def create_post(post: PostCreateSchema) -> dict:
    response = {
        'id': len(fake_db),
        'title': post.title,
        'text': post.text,
        'pub_date': post.pub_date,
        'author': post.author,
        'location': post.location,
        'category': post.category,
        'created_at': datetime.now(),
        'is_published': post.is_published,
    }
    fake_db.append(response)
    return PostResponseSchema.model_validate(obj=response)


@router.put(
    '/update/{post_id}',
    status_code=status.HTTP_200_OK,
    response_model=PostResponseSchema,
)
def update_post(post_id: int, post: PostUpdateSchema) -> dict:
    if post_id >= len(fake_db):
        raise HTTPException(
            detail='Пост не найден',
            status_code=status.HTTP_404_NOT_FOUND,
        )
    response = fake_db[post_id]
    response['title'] = post.title
    response['text'] = post.text
    response['location'] = post.location
    response['category'] = post.category
    response['is_published'] = post.is_published
    return PostResponseSchema.model_validate(obj=response)


@router.delete('/delete/{post_id}', status_code=status.HTTP_200_OK)
def delete_post(post_id: int):
    if post_id >= len(fake_db):
        raise HTTPException(
            detail='Пост не найден',
            status_code=status.HTTP_404_NOT_FOUND,
        )
    fake_db.pop(post_id)
    return {'message': 'Пост успешно удален'}
