from typing import Optional

from app.context.auth.application.commands import LoginCommand
from app.context.auth.application.contracts import (
    GetSessionHandlerContract,
    LoginHandlerContract,
)
from app.context.auth.application.dto import LoginHandlerResultDTO
from app.context.auth.application.query import GetSessionQuery
from app.context.user.application.contracts.find_user_query_handler_contract import (
    FindUserHandlerContract,
)
from app.context.user.application.queries.find_user_query import FindUserQuery


class LoginHandler(LoginHandlerContract):
    _user_service: FindUserHandlerContract
    _session_service: GetSessionHandlerContract

    def __init__(
        self,
        user_service: FindUserHandlerContract,
        session_service: GetSessionHandlerContract,
    ):
        self._user_service = user_service
        self._session_service = session_service
        pass

    async def handle(self, command: LoginCommand) -> Optional[LoginHandlerResultDTO]:
        user = await self._user_service.handle(FindUserQuery(email=command.email))

        if user is None:
            print("Bolocks")
            return

        session = await self._session_service.handle(
            GetSessionQuery(user_id=user.user_id)
        )
        print(session)

        print("---end---")
