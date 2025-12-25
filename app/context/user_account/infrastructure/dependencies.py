from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.context.user_account.application.contracts.create_account_handler_contract import (
    CreateAccountHandlerContract,
)
from app.context.user_account.application.handlers.create_account_handler import (
    CreateAccountHandler,
)
from app.context.user_account.domain.contracts.infrastructure.user_account_repository_contract import (
    UserAccountRepositoryContract,
)
from app.context.user_account.domain.contracts.services.create_account_service_contract import (
    CreateAccountServiceContract,
)
from app.context.user_account.domain.services.create_account_service import CreateAccountService
from app.context.user_account.infrastructure.repositories.user_account_repository import (
    UserAccountRepository,
)
from app.shared.infrastructure.database import get_db


def get_user_account_repository(
    db: AsyncSession = Depends(get_db),
) -> UserAccountRepositoryContract:
    """UserAccountRepository dependency injection"""
    return UserAccountRepository(db)


def get_create_account_service(
    account_repository: UserAccountRepositoryContract = Depends(get_user_account_repository),
) -> CreateAccountServiceContract:
    """CreateAccountService dependency injection"""
    return CreateAccountService(account_repository)


def get_create_account_handler(
    service: CreateAccountServiceContract = Depends(get_create_account_service),
) -> CreateAccountHandlerContract:
    """CreateAccountHandler dependency injection"""
    return CreateAccountHandler(service)
