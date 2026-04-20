from datetime import datetime

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.users import UserRepository
from infrastructure.sqlite.models.users import User
from schemas.users import UserSchema
from resources.auth import get_password_hash
from core.exceptions.database_exceptions import EntityAlreadyExistsException


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
            # Check if user already exists
            try:
                existing_user = self._repo.get_by_username(
                    session=session, username=username
                )
                if existing_user:
                    raise EntityAlreadyExistsException(
                        entity_name='User',
                        detail=f'Пользователь с username "{username}" уже существует'
                    )
            except Exception:
                pass  # User doesn't exist, continue

            # Create new user with hashed password
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
