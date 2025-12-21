from typing import Optional

from app.context.auth.application.commands import LoginCommand
from app.context.auth.application.contracts import LoginHandlerContract
from app.context.auth.application.dto import LoginHandlerResultDTO
from app.context.auth.domain.contracts import LoginServiceContract
from app.context.user.domain.value_objects import Email, Password


class LoginHandler(LoginHandlerContract):
    _login_service: LoginServiceContract

    def __init__(self, login_service: LoginServiceContract):
        self._login_service = login_service
        pass

    async def handle(self, command: LoginCommand) -> Optional[LoginHandlerResultDTO]:
        email = Email(command.email)
        password = Password.keep_plain(command.password)

        result = await self._login_service.handle(email, password)
        print(result)
        print("---end---")
