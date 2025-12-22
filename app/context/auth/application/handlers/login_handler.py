from typing import Optional

from app.context.auth.application.commands import LoginCommand
from app.context.auth.application.contracts import (
    LoginHandlerContract,
)
from app.context.auth.application.dto import LoginHandlerResultDTO
from app.context.auth.domain.contracts import LoginServiceContract
from app.context.auth.domain.dto import AuthUserDTO
from app.context.auth.domain.value_objects import AuthEmail, AuthPassword, AuthUserID
from app.context.user.application.contracts import FindUserHandlerContract
from app.context.user.application.queries import FindUserQuery


class LoginHandler(LoginHandlerContract):
    _user_handler: FindUserHandlerContract
    _login_service: LoginServiceContract

    def __init__(
        self, user_handler: FindUserHandlerContract, login_service: LoginServiceContract
    ):
        self._user_handler = user_handler
        self._login_service = login_service
        pass

    async def handle(self, command: LoginCommand) -> Optional[LoginHandlerResultDTO]:
        user = await self._user_handler.handle(FindUserQuery(email=command.email))
        if user is None:
            # Error invalid login attempt
            return

        res = await self._login_service.handle(
            user_password=AuthPassword(command.password),
            db_user=AuthUserDTO(
                user_id=AuthUserID(user.user_id),
                email=AuthEmail(user.email),
                password=AuthPassword.from_hash(user.password),
            ),
        )

        print(res)

        print("---end---")
