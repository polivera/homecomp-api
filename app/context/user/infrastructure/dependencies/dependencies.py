from sqlalchemy.ext.asyncio import AsyncSession

from app.context.user.application.contracts import FindUserHandlerContract
from app.context.user.application.handlers import FindUserHandler
from app.context.user.domain.contracts.infrastructure import UserRepositoryContract
from app.context.user.infrastructure.repositories import UserRepository
from app.shared.domain.contracts import LoggerContract


def find_user_handler_factory(db: AsyncSession, logger: LoggerContract) -> FindUserHandlerContract:
    return FindUserHandler(_get_user_repository(db))


def _get_user_repository(db: AsyncSession) -> UserRepositoryContract:
    return UserRepository(db)
