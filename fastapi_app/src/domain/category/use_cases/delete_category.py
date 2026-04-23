from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.categories import CategoryRepository
from core.exceptions.domain_exceptions import ForbiddenActionException


class DeleteCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int, is_superuser: bool = False) -> bool:
        if not is_superuser:
            raise ForbiddenActionException()
        
        with self._database.session() as session:
            self._repo.delete(session=session, id=category_id)

        return True
