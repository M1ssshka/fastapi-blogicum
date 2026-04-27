class BaseDatabaseException(Exception):
    def __init__(self, detail: str | None = None) -> None:
        self._detail = detail


class EntityNotFoundException(BaseDatabaseException):
    pass


class EntityAlreadyExistsException(BaseDatabaseException):
    pass


class UserNotFoundException(BaseDatabaseException):
    pass


class PostNotFoundException(BaseDatabaseException):
    pass


class CategoryNotFoundException(BaseDatabaseException):
    pass


class LocationNotFoundException(BaseDatabaseException):
    pass


class CategorySlugConflictException(BaseDatabaseException):
    pass


class LocationNameConflictException(BaseDatabaseException):
    pass
