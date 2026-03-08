from domain.user.use_cases.get_user_by_username import GetUserByUsernameUseCase
from domain.category.use_cases.get_category_by_slug import (
    GetCategoryBySlugUseCase,
)
from domain.location.use_cases.get_location_by_id import GetLocationByIdUseCase
from domain.post.use_cases.get_post_by_id import GetPostByIdUseCase
from domain.comment.use_cases.get_comment_by_id import GetCommentByIdUseCase


def get_get_user_by_username_use_case() -> GetUserByUsernameUseCase:
    return GetUserByUsernameUseCase()


def get_get_category_by_slug_use_case() -> GetCategoryBySlugUseCase:
    return GetCategoryBySlugUseCase()


def get_get_location_by_id_use_case() -> GetLocationByIdUseCase:
    return GetLocationByIdUseCase()


def get_get_post_by_id_use_case() -> GetPostByIdUseCase:
    return GetPostByIdUseCase()


def get_get_comment_by_id_use_case() -> GetCommentByIdUseCase:
    return GetCommentByIdUseCase()
