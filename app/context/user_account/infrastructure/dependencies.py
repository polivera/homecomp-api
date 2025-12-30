from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.context.user_account.application.contracts.create_account_handler_contract import (
    CreateAccountHandlerContract,
)
from app.context.user_account.application.contracts.delete_account_handler_contract import (
    DeleteAccountHandlerContract,
)
from app.context.user_account.application.contracts.find_account_by_id_handler_contract import (
    FindAccountByIdHandlerContract,
)
from app.context.user_account.application.contracts.find_accounts_by_user_handler_contract import (
    FindAccountsByUserHandlerContract,
)
from app.context.user_account.application.contracts.update_account_handler_contract import (
    UpdateAccountHandlerContract,
)
from app.context.user_account.domain.contracts.infrastructure.user_account_repository_contract import (
    UserAccountRepositoryContract,
)
from app.context.user_account.domain.contracts.services.create_account_service_contract import (
    CreateAccountServiceContract,
)
from app.context.user_account.domain.contracts.services.update_account_service_contract import (
    UpdateAccountServiceContract,
)
from app.shared.domain.contracts import LoggerContract
from app.shared.infrastructure.database import get_db
from app.shared.infrastructure.dependencies import get_logger


def get_user_account_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserAccountRepositoryContract:
    """UserAccountRepository dependency injection"""
    from app.context.user_account.infrastructure.repositories.user_account_repository import (
        UserAccountRepository,
    )

    return UserAccountRepository(db)


# ─────────────────────────────────────────────────────────────────
# COMMAND HANDLERS (Write operations)
# ─────────────────────────────────────────────────────────────────


def get_create_account_service(
    account_repository: Annotated[UserAccountRepositoryContract, Depends(get_user_account_repository)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> CreateAccountServiceContract:
    """CreateAccountService dependency injection"""
    from app.context.user_account.domain.services.create_account_service import (
        CreateAccountService,
    )

    return CreateAccountService(account_repository, logger)


def get_create_account_handler(
    service: Annotated[CreateAccountServiceContract, Depends(get_create_account_service)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> CreateAccountHandlerContract:
    """CreateAccountHandler dependency injection"""
    from app.context.user_account.application.handlers.create_account_handler import (
        CreateAccountHandler,
    )

    return CreateAccountHandler(service, logger)


def get_update_account_service(
    repository: Annotated[UserAccountRepositoryContract, Depends(get_user_account_repository)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> UpdateAccountServiceContract:
    """UpdateAccountService dependency injection"""
    from app.context.user_account.domain.services.update_account_service import (
        UpdateAccountService,
    )

    return UpdateAccountService(repository, logger)


def get_update_account_handler(
    service: Annotated[UpdateAccountServiceContract, Depends(get_update_account_service)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> UpdateAccountHandlerContract:
    """UpdateAccountHandler dependency injection"""
    from app.context.user_account.application.handlers.update_account_handler import (
        UpdateAccountHandler,
    )

    return UpdateAccountHandler(service, logger)


def get_delete_account_handler(
    repository: Annotated[UserAccountRepositoryContract, Depends(get_user_account_repository)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> DeleteAccountHandlerContract:
    """DeleteAccountHandler dependency injection"""
    from app.context.user_account.application.handlers.delete_account_handler import (
        DeleteAccountHandler,
    )

    return DeleteAccountHandler(repository, logger)


# ─────────────────────────────────────────────────────────────────
# QUERY HANDLERS (Read operations)
# ─────────────────────────────────────────────────────────────────


def get_find_account_by_id_handler(
    repository: Annotated[UserAccountRepositoryContract, Depends(get_user_account_repository)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> FindAccountByIdHandlerContract:
    """FindAccountByIdHandler dependency injection"""
    from app.context.user_account.application.handlers.find_account_by_id_handler import (
        FindAccountByIdHandler,
    )

    return FindAccountByIdHandler(repository, logger)


def get_find_accounts_by_user_handler(
    repository: Annotated[UserAccountRepositoryContract, Depends(get_user_account_repository)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
) -> FindAccountsByUserHandlerContract:
    """FindAccountsByUserHandler dependency injection"""
    from app.context.user_account.application.handlers.find_accounts_by_user_handler import (
        FindAccountsByUserHandler,
    )

    return FindAccountsByUserHandler(repository, logger)
