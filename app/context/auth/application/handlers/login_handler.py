from typing import Optional

from app.context.auth.application.commands import LoginCommand
from app.context.auth.application.contracts import LoginHandlerContract
from app.context.auth.application.dto import LoginHandlerResultDTO
from app.context.user.application.contracts.find_user_query_handler_contract import (
    FindUserHandlerContract,
)
from app.context.user.application.queries.find_user_query import FindUserQuery


class LoginHandler(LoginHandlerContract):
    _user_service: FindUserHandlerContract

    def __init__(self, user_service: FindUserHandlerContract):
        self._user_service = user_service
        pass

    async def handle(self, command: LoginCommand) -> Optional[LoginHandlerResultDTO]:
        user = await self._user_service.handle(FindUserQuery(email=command.email))
        print(command)
        print(user)
        print("---end---")
