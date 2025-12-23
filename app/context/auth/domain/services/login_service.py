import asyncio
from datetime import datetime, timedelta

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


class LoginService(LoginServiceContract):
    _session_repo: SessionRepositoryContract

    def __init__(self, session_repo: SessionRepositoryContract):
        self._session_repo = session_repo

    async def handle(
        self, user_password: AuthPassword, db_user: AuthUserDTO
    ) -> SessionToken:
        session = await self._session_repo.getSession(user_id=db_user.user_id)

        if session is None:
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
            # Account is blocked
            raise AccountBlockedException(session.blocked_until.toString())

        if not db_user.password.verify(user_password.value):
            # Increment failed attempts
            new_attempts = FailedLoginAttempts(session.failed_attempts.value + 1)

            # Block account if max attempts reached
            blocked_until = None
            if new_attempts.hasReachMaxAttempts():
                blocked_until = BlockedTime(datetime.now() + timedelta(minutes=15))

            await self._session_repo.updateSession(
                SessionDTO(
                    user_id=db_user.user_id,
                    token=None,
                    failed_attempts=new_attempts,
                    blocked_until=blocked_until,
                )
            )

            # Seep to avoid brute force attempts
            await asyncio.sleep(new_attempts.getAttemptDelay())

            raise InvalidCredentialsException()

        # Create token and reset failed attempts
        new_token = SessionToken.generate()

        await self._session_repo.updateSession(
            SessionDTO(
                user_id=db_user.user_id,
                token=new_token,
                failed_attempts=FailedLoginAttempts(0),
                blocked_until=None,
            )
        )

        return new_token
