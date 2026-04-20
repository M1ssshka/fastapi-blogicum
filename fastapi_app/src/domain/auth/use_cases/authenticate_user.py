from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from schemas.users import UserSchema
from resources.auth import verify_password
from core.exceptions.database_exceptions import EntityNotFoundException
from core.exceptions.domain_exceptions import (
    UserNotFoundByLoginException,
    WrongPasswordException,
)


class AuthenticateUserUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = UserRepository()

    async def execute(
        self,
        username: str,
        password: str,
    ) -> UserSchema:
        try:
            with self._database.session() as session:
                user = self._repo.get_by_username(
                    session=session, username=username
                )
        except EntityNotFoundException:
            error = UserNotFoundByLoginException(username=username)
            raise error

        if not verify_password(
            plain_password=password, hashed_password=user.password
        ):
            error = WrongPasswordException()
            raise error

        return UserSchema.model_validate(obj=user)
