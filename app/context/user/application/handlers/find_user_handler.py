from typing import Optional

from app.context.user.application.contracts import FindUserHandlerContract
from app.context.user.application.dto import UserContextDTO
from app.context.user.application.queries import FindUserQuery
from app.context.user.domain.contracts.infrastrutcure import UserRepositoryContract
from app.context.user.domain.value_objects import Email, UserID


class FindUserHandler(FindUserHandlerContract):
    def __init__(self, user_repo: UserRepositoryContract):
        self.user_repo = user_repo

    async def handle(self, query: FindUserQuery) -> Optional[UserContextDTO]:
        email = Email(value=query.email) if query.email is not None else None
        user_id = UserID(value=query.user_id) if query.user_id is not None else None
        res = await self.user_repo.find_user(user_id=user_id, email=email)
        return (
            UserContextDTO(
                user_id=res.user_id.value,
                email=res.email.value,
                password=res.password.value,
            )
            if res is not None
            else None
        )
