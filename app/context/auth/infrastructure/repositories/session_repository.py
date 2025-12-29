
from sqlalchemy import select, update
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
        self, user_id: AuthUserID | None = None, token: SessionToken | None = None
    ) -> SessionDTO | None:
        stmt = select(SessionModel)
        if user_id is not None:
            stmt = stmt.where(SessionModel.user_id == user_id.value)
        if token is not None:
            stmt = stmt.where(SessionModel.token == token.value)

        res = await self._db.execute(stmt)
        return SessionMapper.toDTO(res.scalar_one_or_none())

    async def createSession(self, session: SessionDTO) -> SessionDTO:
        session_model = SessionModel(
            user_id=session.user_id.value,
            token=session.token.value if session.token is not None else None,
            failed_attempts=session.failed_attempts.value,
            blocked_until=session.blocked_until.value
            if session.blocked_until is not None
            else None,
        )

        self._db.add(session_model)
        await self._db.commit()
        await self._db.refresh(session_model)
        dto = SessionMapper.toDTO(session_model)
        if dto is None:
            # TODO: Valid exception
            raise Exception("send a valid exception here")

        return dto

    async def updateSession(self, session: SessionDTO) -> SessionDTO:
        stmt = (
            update(SessionModel)
            .where(SessionModel.user_id == session.user_id.value)
            .values(
                token=session.token.value if session.token is not None else None,
                failed_attempts=session.failed_attempts.value,
                blocked_until=session.blocked_until.value
                if session.blocked_until is not None
                else None,
            )
        )
        await self._db.execute(stmt)
        await self._db.commit()

        return session
