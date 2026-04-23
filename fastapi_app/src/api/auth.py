from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from schemas.auth import Token
from schemas.users import UserCreateSchema, UserResponseSchema
from domain.auth.use_cases.authenticate_user import (
    AuthenticateUserUseCase,
)
from domain.auth.use_cases.create_access_token import (
    CreateAccessTokenUseCase,
)
from domain.user.use_cases.create_user import CreateUserUseCase
from core.exceptions.domain_exceptions import (
    WrongPasswordException,
    UserNotFoundByLoginException,
    UserAlreadyExistsException,
)
from api.depends import (
    create_access_token_use_case,
    authenticate_user_use_case,
    get_create_user_use_case,
)

router = APIRouter()


@router.post('/token', response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_use_case: Annotated[
        AuthenticateUserUseCase, Depends(authenticate_user_use_case)
    ],
    create_token_use_case: CreateAccessTokenUseCase = Depends(
        create_access_token_use_case
    ),
) -> Token:
    try:
        user = await auth_use_case.execute(
            username=form_data.username, password=form_data.password
        )
    except WrongPasswordException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.get_detail(),
            headers={'WWW-Authenticate': 'Bearer'},
        )
    except UserNotFoundByLoginException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )

    access_token = await create_token_use_case.execute(username=user.username)

    return Token(access_token=access_token, token_type='bearer')


@router.post(
    '/register',
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user_data: UserCreateSchema,
    create_user_use_case: CreateUserUseCase = Depends(
        get_create_user_use_case
    ),
) -> UserResponseSchema:
    try:
        user = await create_user_use_case.execute(
            username=user_data.username,
            password=user_data.password,
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
        )
        return UserResponseSchema.model_validate(obj=user)
    except UserAlreadyExistsException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exc.get_detail(),
        )
