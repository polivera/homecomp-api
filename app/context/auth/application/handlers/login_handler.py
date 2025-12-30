from app.context.auth.application.commands import LoginCommand
from app.context.auth.application.contracts import (
    LoginHandlerContract,
)
from app.context.auth.application.dto import (
    LoginHandlerResultDTO,
    LoginHandlerResultStatus,
)
from app.context.auth.domain.contracts import LoginServiceContract
from app.context.auth.domain.dto import AuthUserDTO
from app.context.auth.domain.exceptions import (
    AccountBlockedException,
    InvalidCredentialsException,
)
from app.context.auth.domain.value_objects import AuthEmail, AuthPassword, AuthUserID
from app.context.user.application.contracts import FindUserHandlerContract
from app.context.user.application.queries import FindUserQuery
from app.shared.domain.contracts import LoggerContract


class LoginHandler(LoginHandlerContract):
    _user_handler: FindUserHandlerContract
    _login_service: LoginServiceContract
    _logger: LoggerContract

    def __init__(
        self,
        user_handler: FindUserHandlerContract,
        login_service: LoginServiceContract,
        logger: LoggerContract,
    ):
        self._user_handler = user_handler
        self._login_service = login_service
        self._logger = logger

    async def handle(self, command: LoginCommand) -> LoginHandlerResultDTO:
        self._logger.debug("Handling login command", email=command.email)

        user = await self._user_handler.handle(FindUserQuery(email=command.email))
        if user is None or user.error_code is not None:
            self._logger.debug("User not found", email=command.email)
            return LoginHandlerResultDTO(
                status=LoginHandlerResultStatus.INVALID_CREDENTIALS,
                error_msg="Invalid username or password",
            )

        if user.user_id is None or user.email is None or user.password is None:
            self._logger.error("Invalid user data retrieved from database", email=command.email)
            return LoginHandlerResultDTO(
                status=LoginHandlerResultStatus.UNEXPECTED_ERROR,
                error_msg="Invalid user data",
            )

        try:
            user_token = await self._login_service.handle(
                user_password=AuthPassword(command.password),
                db_user=AuthUserDTO(
                    user_id=AuthUserID(user.user_id),
                    email=AuthEmail(user.email),
                    password=AuthPassword.from_hash(user.password),
                ),
            )

            self._logger.debug("Login service succeeded", email=command.email, user_id=user.user_id)

            return LoginHandlerResultDTO(
                status=LoginHandlerResultStatus.SUCCESS,
                token=user_token.value,
                user_id=user.user_id,
            )
        except AccountBlockedException as abe:
            self._logger.info(
                "Account blocked",
                email=command.email,
                blocked_until=abe.blocked_until.isoformat() if abe.blocked_until else None,
            )
            return LoginHandlerResultDTO(
                status=LoginHandlerResultStatus.ACCOUNT_BLOCKED,
                retry_after=abe.blocked_until,
                error_msg="Account is blocked, try again later",
            )
        except InvalidCredentialsException:
            self._logger.debug("Invalid credentials provided", email=command.email)
            return LoginHandlerResultDTO(
                status=LoginHandlerResultStatus.INVALID_CREDENTIALS,
                error_msg="Invalid username or password",
            )
        except Exception as e:
            self._logger.error("Unexpected error during login", email=command.email, error=str(e))
            return LoginHandlerResultDTO(
                status=LoginHandlerResultStatus.UNEXPECTED_ERROR,
                error_msg="Unexpected error",
            )
