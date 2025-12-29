from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.context.user.application.contracts import FindUserHandlerContract
from app.context.user.application.handlers import FindUserHandler
from app.context.user.domain.contracts.infrastructure import UserRepositoryContract
from app.context.user.infrastructure.repositories import UserRepository
from app.shared.infrastructure.database import get_db


def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepositoryContract:
    """
    Initialize user repository
    """
    return UserRepository(db)


def get_find_user_query_handler(
    user_repo: UserRepositoryContract = Depends(get_user_repository),
) -> FindUserHandlerContract:
    """
    Initialize FindUserHandler
    """
    return FindUserHandler(user_repo)
