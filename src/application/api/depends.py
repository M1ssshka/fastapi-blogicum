# User
from application.domain.user.use_cases.activate_user import ActivateUserUseCase
from application.domain.user.use_cases.deactivate_user import (
    DeactivateUserUseCase,
)
from application.domain.user.use_cases.get_user_by_username import (
    GetUserByUsernameUseCase,
)
from application.domain.user.use_cases.create_user import CreateUserUseCase
from application.domain.user.use_cases.update_user import UpdateUserUseCase

# Category
from application.domain.category.use_cases.get_category_by_slug import (
    GetCategoryBySlugUseCase,
)
from application.domain.category.use_cases.get_category_by_id import (
    GetCategoryByIdUseCase,
)
from application.domain.category.use_cases.create_category import (
    CreateCategoryUseCase,
)
from application.domain.category.use_cases.update_category import (
    UpdateCategoryUseCase,
)
from application.domain.category.use_cases.delete_category import (
    DeleteCategoryUseCase,
)
from application.domain.category.use_cases.get_all_categories import (
    GetAllCategoriesUseCase,
)

# Location
from application.domain.location.use_cases.get_location_by_id import (
    GetLocationByIdUseCase,
)
from application.domain.location.use_cases.create_location import (
    CreateLocationUseCase,
)
from application.domain.location.use_cases.update_location import (
    UpdateLocationUseCase,
)
from application.domain.location.use_cases.delete_location import (
    DeleteLocationUseCase,
)
from application.domain.location.use_cases.get_all_locations import (
    GetAllLocationsUseCase,
)

# Post
from application.domain.post.use_cases.get_post_by_id import GetPostByIdUseCase
from application.domain.post.use_cases.create_post import CreatePostUseCase
from application.domain.post.use_cases.update_post import UpdatePostUseCase
from application.domain.post.use_cases.delete_post import DeletePostUseCase
from application.domain.post.use_cases.get_all_posts import GetAllPostsUseCase
from application.domain.post.use_cases.add_post_image import (
    AddPostImageUseCase,
)
from application.domain.post.use_cases.get_post_image import (
    GetPostImageUseCase,
)

# Comment
from application.domain.comment.use_cases.get_comment_by_id import (
    GetCommentByIdUseCase,
)
from application.domain.comment.use_cases.create_comment import (
    CreateCommentUseCase,
)
from application.domain.comment.use_cases.update_comment import (
    UpdateCommentUseCase,
)
from application.domain.comment.use_cases.delete_comment import (
    DeleteCommentUseCase,
)
from application.domain.comment.use_cases.get_all_comments import (
    GetAllCommentsUseCase,
)


from application.domain.auth.use_cases.authenticate_user import (
    AuthenticateUserUseCase,
)
from application.domain.auth.use_cases.create_access_token import (
    CreateAccessTokenUseCase,
)
from application.domain.auth.use_cases.create_refresh_token import (
    CreateRefreshTokenUseCase,
)
from application.domain.auth.use_cases.refresh_tokens import (
    RefreshTokensUseCase,
)


# User factories
def get_get_user_by_username_use_case() -> GetUserByUsernameUseCase:
    return GetUserByUsernameUseCase()


def get_create_user_use_case() -> CreateUserUseCase:
    return CreateUserUseCase()


def get_update_user_use_case() -> UpdateUserUseCase:
    return UpdateUserUseCase()


def get_deactivate_user_use_case() -> DeactivateUserUseCase:
    return DeactivateUserUseCase()


def get_activate_user_use_case() -> ActivateUserUseCase:
    return ActivateUserUseCase()


# Category factories
def get_get_category_by_slug_use_case() -> GetCategoryBySlugUseCase:
    return GetCategoryBySlugUseCase()


def get_get_category_by_id_use_case() -> GetCategoryByIdUseCase:
    return GetCategoryByIdUseCase()


def get_create_category_use_case() -> CreateCategoryUseCase:
    return CreateCategoryUseCase()


def get_update_category_use_case() -> UpdateCategoryUseCase:
    return UpdateCategoryUseCase()


def get_delete_category_use_case() -> DeleteCategoryUseCase:
    return DeleteCategoryUseCase()


def get_get_all_categories_use_case() -> GetAllCategoriesUseCase:
    return GetAllCategoriesUseCase()


# Location factories
def get_get_location_by_id_use_case() -> GetLocationByIdUseCase:
    return GetLocationByIdUseCase()


def get_create_location_use_case() -> CreateLocationUseCase:
    return CreateLocationUseCase()


def get_update_location_use_case() -> UpdateLocationUseCase:
    return UpdateLocationUseCase()


def get_delete_location_use_case() -> DeleteLocationUseCase:
    return DeleteLocationUseCase()


def get_get_all_locations_use_case() -> GetAllLocationsUseCase:
    return GetAllLocationsUseCase()


# Post factories
def get_get_post_by_id_use_case() -> GetPostByIdUseCase:
    return GetPostByIdUseCase()


def get_create_post_use_case() -> CreatePostUseCase:
    return CreatePostUseCase()


def get_update_post_use_case() -> UpdatePostUseCase:
    return UpdatePostUseCase()


def get_delete_post_use_case() -> DeletePostUseCase:
    return DeletePostUseCase()


def get_get_all_posts_use_case() -> GetAllPostsUseCase:
    return GetAllPostsUseCase()


def get_add_post_image_use_case() -> AddPostImageUseCase:
    return AddPostImageUseCase()


def get_get_post_image_use_case() -> GetPostImageUseCase:
    return GetPostImageUseCase()


# Comment factories
def get_get_comment_by_id_use_case() -> GetCommentByIdUseCase:
    return GetCommentByIdUseCase()


def get_create_comment_use_case() -> CreateCommentUseCase:
    return CreateCommentUseCase()


def get_update_comment_use_case() -> UpdateCommentUseCase:
    return UpdateCommentUseCase()


def get_delete_comment_use_case() -> DeleteCommentUseCase:
    return DeleteCommentUseCase()


def get_get_all_comments_use_case() -> GetAllCommentsUseCase:
    return GetAllCommentsUseCase()


def authenticate_user_use_case() -> AuthenticateUserUseCase:
    return AuthenticateUserUseCase()


def create_access_token_use_case() -> CreateAccessTokenUseCase:
    return CreateAccessTokenUseCase()


def create_refresh_token_use_case() -> CreateRefreshTokenUseCase:
    return CreateRefreshTokenUseCase()


def refresh_tokens_use_case() -> RefreshTokensUseCase:
    return RefreshTokensUseCase()
