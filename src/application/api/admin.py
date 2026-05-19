from fastapi import APIRouter, status, Depends, HTTPException
from application.domain.user.use_cases.activate_user import ActivateUserUseCase
from application.domain.user.use_cases.update_user import UpdateUserUseCase

from application.domain.user.use_cases.deactivate_user import (
    DeactivateUserUseCase,
)
from application.schemas.users import UserSchema, UserUpdateSchema
from application.schemas.base import UsernameStr

from application.core.exceptions.domain_exceptions import (
    ForbiddenActionException,
    UserNotFoundByLoginException,
)
from application.services.auth import AuthService

from application.api.depends import (
    get_activate_user_use_case,
    get_deactivate_user_use_case,
    get_update_user_use_case,
)

router = APIRouter()


@router.post(
    '/admin/user/activate/{username}',
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
)
async def activate_user(
    username: UsernameStr,
    user: UserSchema = Depends(AuthService.get_current_user),
    use_case: ActivateUserUseCase = Depends(get_activate_user_use_case),
) -> UserSchema:
    if not user.is_superuser:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail='Доступ к данной ручке разрешен только администраторам',
        )
    try:
        return await use_case.execute(
            target_username=username, current_user=user
        )
    except UserNotFoundByLoginException as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=exc.get_detail())
    except ForbiddenActionException as exc:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=exc.get_detail())


@router.post(
    '/admin/user/deactivate/{username}',
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
)
async def deactivate_user(
    username: UsernameStr,
    user: UserSchema = Depends(AuthService.get_current_user),
    use_case: DeactivateUserUseCase = Depends(get_deactivate_user_use_case),
) -> UserSchema:
    if not user.is_superuser:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail='Доступ к данной ручке разрешен только администраторам',
        )
    try:
        return await use_case.execute(
            target_username=username,
            current_user=user,
        )
    except UserNotFoundByLoginException as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=exc.get_detail())
    except ForbiddenActionException as exc:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=exc.get_detail())


@router.put(
    '/admin/user/edit/{username}',
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
)
async def edit_user(
    username: UsernameStr,
    update_data: UserUpdateSchema,
    user: UserSchema = Depends(AuthService.get_current_user),
    use_case: UpdateUserUseCase = Depends(get_update_user_use_case),
) -> UserSchema:
    if not user.is_superuser:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail='Доступ к данной ручке разрешен только администраторам',
        )
    try:
        return await use_case.execute(
            target_username=username,
            current_user=user,
            update_data=update_data,
        )
    except ForbiddenActionException as exc:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=exc.get_detail())
    except UserNotFoundByLoginException as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=exc.get_detail())
