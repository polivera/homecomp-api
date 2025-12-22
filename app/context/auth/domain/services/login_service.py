from app.context.auth.domain.contracts import LoginServiceContract
from app.context.auth.domain.value_objects import AuthEmail, AuthPassword
from app.context.user.application.contracts import FindUserHandlerContract
from app.context.user.application.queries import FindUserQuery


class LoginService(LoginServiceContract):
    def __init__(self, user_service: FindUserHandlerContract):
        self._user_service = user_service

    async def handle(self, email: AuthEmail, plain_password: AuthPassword):
        user = await self._user_service.handle(FindUserQuery(email=email.value))

        if user is not None and AuthPassword.from_hash(user.password).verify(
            plain_password.value
        ):
            print("login success")

        else:
            print("User does not exist")

        pass
