from domain.user.use_cases.get_user_by_login import GetUserByLoginUseCase
from domain.user.use_cases.get_category_by_slug import GetCategoryBySlug


def get_get_user_by_login_use_case() -> GetUserByLoginUseCase:
    return GetUserByLoginUseCase()


def get_get_category_by_slug_use_case() -> GetCategoryBySlug:
    return GetCategoryBySlug()
