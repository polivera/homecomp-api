from app.context.auth.domain.contracts import SessionRepositoryContract
from app.context.auth.domain.value_objects import FailedLoginAttempts
from app.context.user.domain.value_objects import Email
from app.shared.infrastructure.database import AsyncSessionLocal


class SessionRepository(SessionRepositoryContract):
    _db: AsyncSessionLocal

    def __init__(self, db: AsyncSessionLocal):
        self.db = db

    async def getLoginAttepmps(self, email: Email) -> FailedLoginAttempts:
        pass
