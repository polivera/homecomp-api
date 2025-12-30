from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.context.auth.application.contracts import (
    LoginHandlerContract,
)
from app.context.auth.application.contracts.get_session_handler_contract import (
    GetSessionHandlerContract,
)
from app.context.auth.application.handlers import LoginHandler
from app.context.auth.application.handlers.get_session_handler import GetSessionHandler
from app.context.auth.domain.contracts import (
    LoginServiceContract,
    SessionRepositoryContract,
)
from app.context.auth.domain.services import LoginService
from app.context.auth.infrastructure.repositories import SessionRepository
from app.context.user.application.contracts import (
    FindUserHandlerContract,
)
from app.context.user.infrastructure.dependencies import (
    get_find_user_query_handler,
)
from app.shared.domain.contracts import LoggerContract
from app.shared.infrastructure.database import get_db
from app.shared.infrastructure.dependencies import get_logger


def get_session_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SessionRepositoryContract:
    return SessionRepository(db)


def get_login_service(
    session_repo: Annotated[SessionRepositoryContract, Depends(get_session_repository)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> LoginServiceContract:
    """
    LoginService dependency injection
    """
    return LoginService(session_repo, logger)


def get_session_handler(
    session_repo: Annotated[SessionRepository, Depends(get_session_repository)],
) -> GetSessionHandlerContract:
    return GetSessionHandler(session_repo)


def get_login_handler(
    user_query_handler: Annotated[FindUserHandlerContract, Depends(get_find_user_query_handler)],
    login_service: Annotated[LoginServiceContract, Depends(get_login_service)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> LoginHandlerContract:
    """
    LoginHandler dependency injection
    """
    return LoginHandler(user_query_handler, login_service, logger)
