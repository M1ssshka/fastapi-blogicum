from datetime import datetime

from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.users import UserRepository
from application.infrastructure.database.models.users import User
from application.schemas.users import UserSchema
from application.resources.auth import get_password_hash
from application.core.exceptions.domain_exceptions import UserAlreadyExistsException


class CreateUserUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = UserRepository()

    async def execute(
        self,
        username: str,
        password: str,
        email: str | None = None,
        first_name: str = '',
        last_name: str = '',
    ) -> UserSchema:
        with self._database.session() as session:
            existing_user = self._repo.get_by_username(
                session=session, username=username
            )
            if existing_user:
                raise UserAlreadyExistsException(username=username)

            user = User(
                username=username,
                password=get_password_hash(password),
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_superuser=False,
                is_staff=False,
                is_active=True,
                date_joined=datetime.now(),
                last_login=None,
            )

            session.add(user)
            session.commit()
            session.refresh(user)

            return UserSchema.model_validate(obj=user)
