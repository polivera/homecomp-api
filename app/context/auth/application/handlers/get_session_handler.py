
from app.context.auth.application.contracts import GetSessionHandlerContract
from app.context.auth.application.dto.get_session_result_dto import GetSessionResultDTO
from app.context.auth.application.queries import GetSessionQuery
from app.context.auth.domain.contracts import SessionRepositoryContract
from app.context.auth.domain.value_objects import AuthUserID, SessionToken


class GetSessionHandler(GetSessionHandlerContract):
    _session_repo: SessionRepositoryContract

    def __init__(self, session_repo: SessionRepositoryContract):
        self._session_repo = session_repo

    async def handle(self, query: GetSessionQuery) -> GetSessionResultDTO | None:
        session = await self._session_repo.getSession(
            user_id=AuthUserID(query.user_id) if query.user_id is not None else None,
            token=SessionToken(query.token) if query.token is not None else None,
        )
        return (
            GetSessionResultDTO(
                user_id=session.user_id.value,
                token=session.token.value if session.token is not None else None,
                failed_attempts=session.failed_attempts.value,
                blocked_until=session.blocked_until.toString()
                if session.blocked_until is not None
                else None,
            )
            if session is not None
            else None
        )
