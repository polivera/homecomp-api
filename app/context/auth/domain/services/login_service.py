from app.context.auth.domain.contracts import LoginServiceContract
from app.context.user.application.contracts import FindUserHandlerContract
from app.context.user.application.queries import FindUserQuery
from app.context.user.domain.value_objects import Email, Password


class LoginService(LoginServiceContract):
    _user_service: FindUserHandlerContract

    def __init__(self, user_service: FindUserHandlerContract):
        self._user_service = user_service

    async def handle(self, email: Email, plain_password: Password):
        user = await self._user_service.handle(FindUserQuery(email=email.value))

        if user is not None and Password.from_hash(user.password).verify(
            plain_password.value
        ):
            print("login success")

        else:
            print("User does not exist")

        pass
