from app.context.auth.domain.contracts import (
    LoginServiceContract,
    SessionRepositoryContract,
)
from app.context.auth.domain.dto import AuthUserDTO
from app.context.auth.domain.value_objects import AuthPassword


class LoginService(LoginServiceContract):
    _session_repo: SessionRepositoryContract

    def __init__(self, session_repo: SessionRepositoryContract):
        self._session_repo = session_repo

    async def handle(self, user_password: AuthPassword, db_user: AuthUserDTO):
        session = await self._session_repo.getSession(user_id=db_user.user_id)

        if session is None:
            # create session, remove the return
            return

        if session.blocked_until is not None and not session.blocked_until.isOver():
            # return you can't log in
            # clear session (don't save yet)
            return

        if not db_user.password.verify(user_password.value):
            # update session attempt or add blocked_until if the attempts pass thet threshold
            # Invalid username or password
            return

        # Create token
        # reset session failed attempts and store the token
        # Return Token

        pass
