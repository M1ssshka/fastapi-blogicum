from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException
from application.schemas.users import UserSchema
from application.schemas.base import UsernameStr

from application.domain.user.use_cases.get_user_by_username import GetUserByUsernameUseCase
from application.core.exceptions.domain_exceptions import UserNotFoundByLoginException
from application.services.auth import AuthService

from application.api.depends import (
    get_get_user_by_username_use_case,
)

router = APIRouter()


@router.get(
    '/user/{username}',
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
)
async def get_user_by_username(
    username: UsernameStr,
    user: UserSchema = Depends(AuthService.get_current_user),
    use_case: GetUserByUsernameUseCase = Depends(
        get_get_user_by_username_use_case
    ),
) -> UserSchema:
    try:
        return await use_case.execute(username=username)
    except UserNotFoundByLoginException as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=exc.get_detail())
