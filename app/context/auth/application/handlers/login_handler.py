from typing import Optional

from app.context.auth.application.commands import LoginCommand
from app.context.auth.application.contracts import LoginHandlerContract
from app.context.auth.application.dto import LoginHandlerResultDTO


class LoginHandler(LoginHandlerContract):
    async def handle(self, command: LoginCommand) -> Optional[LoginHandlerResultDTO]:
        print("This is the actual handler")
        print(command)
