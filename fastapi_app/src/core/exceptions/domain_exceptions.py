class BaseDomainException(Exception):
    def __init__(self, detail: str) -> None:
        self._detail = detail

    def get_detail(self) -> str:
        return self._detail


class UserNotFoundByLoginException(BaseDomainException):
    _exception_text_template = 'Пользователь с логином {username} не найден'

    def __init__(self, username: str) -> None:
        self._exception_text_template = self._exception_text_template.format(
            username=username
        )
        super().__init__(detail=self._exception_text_template)


class PostNotFoundByIdException(BaseDomainException):
    _exception_text_template = 'Пост с id: {id} не найден'

    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(
            id=id
        )
        super().__init__(detail=self._exception_text_template)


class CategoryNotFoundByIdException(BaseDomainException):
    _exception_text_template = 'Категория с id: {id} не найдена'

    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(
            id=id
        )
        super().__init__(detail=self._exception_text_template)


class CategoryNotFoundBySlugException(BaseDomainException):
    _exception_text_template = 'Категория с slug: {slug} не найдена'

    def __init__(self, slug: str) -> None:
        self._exception_text_template = self._exception_text_template.format(
            slug=slug
        )
        super().__init__(detail=self._exception_text_template)


class LocationNotFoundByIdException(BaseDomainException):
    _exception_text_template = 'Локация с id: {id} не найдена'

    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(
            id=id
        )
        super().__init__(detail=self._exception_text_template)


class UserNotFoundByIdException(BaseDomainException):
    _exception_text_template = 'Пользователь с id: {id} не найден'

    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(
            id=id
        )
        super().__init__(detail=self._exception_text_template)


class CommentNotFoundByIdException(BaseDomainException):
    _exception_text_template = 'Комментарий с id: {id} не найден'

    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(
            id=id
        )
        super().__init__(detail=self._exception_text_template)


class CategorySlugAlreadyExistsException(BaseDomainException):
    _exception_text_template = 'Категория с slug: {slug} уже существует'

    def __init__(self, slug: str) -> None:
        self._exception_text_template = self._exception_text_template.format(
            slug=slug
        )
        super().__init__(detail=self._exception_text_template)


class LocationNameAlreadyExistsException(BaseDomainException):
    _exception_text_template = 'Локация с названием: {name} уже существует'

    def __init__(self, name: str) -> None:
        self._exception_text_template = self._exception_text_template.format(
            name=name
        )
        super().__init__(detail=self._exception_text_template)


class WrongPasswordException(BaseDomainException):
    _exception_text = 'Неверный пароль'

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text)
