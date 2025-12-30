import asyncio

from app.context.auth.domain.contracts import (
    LoginServiceContract,
    SessionRepositoryContract,
)
from app.context.auth.domain.dto import AuthUserDTO, SessionDTO
from app.context.auth.domain.exceptions import (
    AccountBlockedException,
    InvalidCredentialsException,
)
from app.context.auth.domain.value_objects import (
    AuthPassword,
    FailedLoginAttempts,
    SessionToken,
)
from app.context.auth.domain.value_objects.blocked_time import BlockedTime
from app.shared.domain.contracts import LoggerContract


class LoginService(LoginServiceContract):
    _session_repo: SessionRepositoryContract
    _logger: LoggerContract

    def __init__(self, session_repo: SessionRepositoryContract, logger: LoggerContract):
        self._session_repo = session_repo
        self._logger = logger

    async def handle(self, user_password: AuthPassword, db_user: AuthUserDTO) -> SessionToken:
        self._logger.debug("Login service started", user_id=db_user.user_id.value, email=db_user.email.value)

        session = await self._session_repo.getSession(user_id=db_user.user_id)

        if session is None:
            self._logger.debug("No existing session, creating new session", user_id=db_user.user_id.value)
            # Create session for first login attempt
            session = await self._session_repo.createSession(
                SessionDTO(
                    user_id=db_user.user_id,
                    token=None,
                    failed_attempts=FailedLoginAttempts(0),
                    blocked_until=None,
                )
            )

        if session.blocked_until is not None and not session.blocked_until.isOver():
            self._logger.warning(
                "Account is blocked",
                user_id=db_user.user_id.value,
                blocked_until=session.blocked_until.value.isoformat(),
            )
            # Account is blocked
            raise AccountBlockedException(session.blocked_until.value)

        if not db_user.password.verify(user_password.value):
            # Increment failed attempts
            new_attempts = FailedLoginAttempts(session.failed_attempts.value + 1)

            self._logger.info(
                "Password verification failed",
                user_id=db_user.user_id.value,
                failed_attempts=new_attempts.value,
            )

            # Block account if max attempts reached
            blocked_until = None
            if new_attempts.hasReachMaxAttempts():
                blocked_until = BlockedTime.setBlocked()
                self._logger.warning(
                    "Max login attempts reached, blocking account",
                    user_id=db_user.user_id.value,
                    blocked_until=blocked_until.value.isoformat(),
                )

            await self._session_repo.updateSession(
                SessionDTO(
                    user_id=db_user.user_id,
                    token=None,
                    failed_attempts=new_attempts,
                    blocked_until=blocked_until,
                )
            )

            # Sleep to avoid brute force attempts
            delay = new_attempts.getAttemptDelay()
            self._logger.debug("Applying login delay", delay_seconds=delay)
            await asyncio.sleep(delay)

            raise InvalidCredentialsException()

        # Create token and reset failed attempts
        new_token = SessionToken.generate()

        self._logger.info(
            "Password verified successfully, creating session token",
            user_id=db_user.user_id.value,
        )

        await self._session_repo.updateSession(
            SessionDTO(
                user_id=db_user.user_id,
                token=new_token,
                failed_attempts=FailedLoginAttempts.reset(),
                blocked_until=None,
            )
        )

        return new_token
