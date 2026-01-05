from sqlalchemy.ext.asyncio import AsyncSession

from app.context.auth.application.contracts import (
    LoginHandlerContract,
)
from app.context.auth.application.handlers import LoginHandler
from app.context.auth.domain.contracts import (
    LoginServiceContract,
    SessionRepositoryContract,
)
from app.context.auth.domain.services import LoginService
from app.shared.domain.contracts import LoggerContract


def login_handler_factory(db: AsyncSession, logger: LoggerContract) -> LoginHandlerContract:
    from app.context.user.infrastructure.dependencies import (
        find_user_handler_factory,
    )

    login_service = _get_login_service(_get_session_repository(db), logger)
    user_query_handler = find_user_handler_factory(db, logger)
    return LoginHandler(user_query_handler, login_service, logger)


def _get_session_repository(db: AsyncSession) -> SessionRepositoryContract:
    from app.context.auth.infrastructure.repositories import SessionRepository

    return SessionRepository(db)


def _get_login_service(session_repository: SessionRepositoryContract, logger: LoggerContract) -> LoginServiceContract:
    return LoginService(session_repository, logger)


# -------------------------------------------------------------------------
