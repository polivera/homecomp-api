from app.context.auth.domain.contracts import SessionRepositoryContract
from app.context.auth.domain.value_objects import FailedLoginAttempts
from app.context.user.domain.value_objects import Email


class SessionRepository(SessionRepositoryContract):
    async def getLoginAttepmps(self, email: Email) -> FailedLoginAttempts:
        pass
