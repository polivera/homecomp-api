from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.context.auth.domain.contracts import SessionRepositoryContract
from app.context.auth.domain.dto.session_dto import SessionDTO
from app.context.auth.domain.value_objects import AuthUserID, SessionToken
from app.context.auth.infrastructure.mappers import SessionMapper
from app.context.auth.infrastructure.models import SessionModel


class SessionRepository(SessionRepositoryContract):
    _db: AsyncSession

    def __init__(self, db: AsyncSession):
        self._db = db

    async def getSession(
        self, user_id: Optional[AuthUserID] = None, token: Optional[SessionToken] = None
    ) -> Optional[SessionDTO]:
        stmt = select(SessionModel)
        if user_id is not None:
            stmt = stmt.where(SessionModel.user_id == user_id.value)
        if token is not None:
            stmt = stmt.where(SessionModel.token == token.value)

        res = await self._db.execute(stmt)
        return SessionMapper.toDTO(res.scalar_one_or_none())
