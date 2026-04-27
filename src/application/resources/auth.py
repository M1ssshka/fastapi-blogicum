from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext


# Support both bcrypt (for new users) and Django's pbkdf2_sha256 (for legacy users)
pwd_context = CryptContext(
    schemes=['bcrypt', 'django_pbkdf2_sha256'], deprecated='auto'
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/token')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
