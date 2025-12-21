from typing import Optional

from app.context.user.application.contracts import FindUserHandlerContract
from app.context.user.application.dto import UserContextDTO
from app.context.user.application.queries import FindUserQuery
from app.context.user.domain.contracts.infrastrutcure import UserRepositoryContract
from app.context.user.domain.value_objects import Email


class FindUserHandler(FindUserHandlerContract):
    def __init__(self, user_repo: UserRepositoryContract):
        self.user_repo = user_repo

    async def handle(self, query: FindUserQuery) -> Optional[UserContextDTO]:
        email = Email(value=query.email) if query.email is not None else None
        res = await self.user_repo.find_user(email)
        return UserContextDTO(id=1, email=res.email.value) if res is not None else None
