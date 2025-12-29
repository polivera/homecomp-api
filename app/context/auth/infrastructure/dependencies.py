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
from app.shared.infrastructure.database import get_db


def get_session_repository(
    db: AsyncSession = Depends(get_db),
) -> SessionRepositoryContract:
    return SessionRepository(db)


def get_login_service(
    session_repo: SessionRepositoryContract = Depends(get_session_repository),
) -> LoginServiceContract:
    """
    LoginService dependency injection
    """
    return LoginService(session_repo)


def get_session_handler(
    session_repo: SessionRepository = Depends(get_session_repository),
) -> GetSessionHandlerContract:
    return GetSessionHandler(session_repo)


def get_login_handler(
    user_query_handler: FindUserHandlerContract = Depends(get_find_user_query_handler),
    login_service: LoginServiceContract = Depends(get_login_service),
) -> LoginHandlerContract:
    """
    LoginHandler dependency injection
    """
    return LoginHandler(user_query_handler, login_service)
