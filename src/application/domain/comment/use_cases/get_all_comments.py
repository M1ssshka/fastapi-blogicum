from typing import List

from application.infrastructure.database.database import database
from application.infrastructure.database.repositories.comments import CommentRepository
from application.schemas.comments import CommentResponse


class GetAllCommentsUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(
        self, limit: int = 100, offset: int = 0
    ) -> List[CommentResponse]:
        async with self._database.session() as session:
            comments = await self._repo.get_all_with_relations(
                session=session, limit=limit, offset=offset
            )

        return [
            CommentResponse.model_validate(obj=comment) for comment in comments
        ]
