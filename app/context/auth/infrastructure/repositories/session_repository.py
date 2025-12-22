from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.context.auth.domain.contracts import SessionRepositoryContract
from app.context.auth.domain.dto.session_dto import SessionDTO
from app.context.auth.domain.value_objects import AuthUserID, SessionToken


class SessionRepository(SessionRepositoryContract):
    _db: AsyncSession

    def __init__(self, db: AsyncSession):
        self.db = db

    async def getSession(
        self, user_id: Optional[AuthUserID] = None, token: Optional[SessionToken] = None
    ) -> Optional[SessionDTO]:
        pass
