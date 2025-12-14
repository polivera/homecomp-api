from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_db
from app.context.auth.infrastructure.repositories.user_repository import UserRepository
from app.context.auth.application.services.user_service import UserService


def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    """
    Dependency to get UserRepository instance.

    This function is called by FastAPI's dependency injection system.
    It receives the database session from get_db() and creates a UserRepository.
    """
    return UserRepository(db)


def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    """
    Dependency to get UserService instance.

    This function is called by FastAPI's dependency injection system.
    It receives the UserRepository from get_user_repository() and creates a UserService.

    Dependency chain:
    get_db() → get_user_repository() → get_user_service()
    """
    return UserService(user_repo)
