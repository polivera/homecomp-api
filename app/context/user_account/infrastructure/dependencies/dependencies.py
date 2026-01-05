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

# ─────────────────────────────────────────────────────────────────
# COMMAND HANDLERS (Write operations)
# ─────────────────────────────────────────────────────────────────


def create_account_handler_factory(
    db: AsyncSession,
    logger: LoggerContract,
) -> CreateAccountHandlerContract:
    """Factory for CreateAccountHandler with all dependencies"""
    from app.context.user_account.application.handlers.create_account_handler import (
        CreateAccountHandler,
    )

    service = _get_create_account_service(_get_user_account_repository(db), logger)
    return CreateAccountHandler(service, logger)


def update_account_handler_factory(
    db: AsyncSession,
    logger: LoggerContract,
) -> UpdateAccountHandlerContract:
    """Factory for UpdateAccountHandler with all dependencies"""
    from app.context.user_account.application.handlers.update_account_handler import (
        UpdateAccountHandler,
    )

    service = _get_update_account_service(_get_user_account_repository(db), logger)
    return UpdateAccountHandler(service, logger)


def delete_account_handler_factory(
    db: AsyncSession,
    logger: LoggerContract,
) -> DeleteAccountHandlerContract:
    """Factory for DeleteAccountHandler with all dependencies"""
    from app.context.user_account.application.handlers.delete_account_handler import (
        DeleteAccountHandler,
    )

    repository = _get_user_account_repository(db)
    return DeleteAccountHandler(repository, logger)


# ─────────────────────────────────────────────────────────────────
# QUERY HANDLERS (Read operations)
# ─────────────────────────────────────────────────────────────────


def find_account_by_id_handler_factory(
    db: AsyncSession,
    logger: LoggerContract,
) -> FindAccountByIdHandlerContract:
    """Factory for FindAccountByIdHandler with all dependencies"""
    from app.context.user_account.application.handlers.find_account_by_id_handler import (
        FindAccountByIdHandler,
    )

    repository = _get_user_account_repository(db)
    return FindAccountByIdHandler(repository, logger)


def find_accounts_by_user_handler_factory(
    db: AsyncSession,
    logger: LoggerContract,
) -> FindAccountsByUserHandlerContract:
    """Factory for FindAccountsByUserHandler with all dependencies"""
    from app.context.user_account.application.handlers.find_accounts_by_user_handler import (
        FindAccountsByUserHandler,
    )

    repository = _get_user_account_repository(db)
    return FindAccountsByUserHandler(repository, logger)


# ─────────────────────────────────────────────────────────────────
# Private helper functions
# ─────────────────────────────────────────────────────────────────


def _get_user_account_repository(db: AsyncSession) -> UserAccountRepositoryContract:
    """Get user account repository instance"""
    from app.context.user_account.infrastructure.repositories.user_account_repository import (
        UserAccountRepository,
    )

    return UserAccountRepository(db)


def _get_create_account_service(
    repository: UserAccountRepositoryContract,
    logger: LoggerContract,
) -> CreateAccountServiceContract:
    """Get create account service instance"""
    from app.context.user_account.domain.services.create_account_service import (
        CreateAccountService,
    )

    return CreateAccountService(repository, logger)


def _get_update_account_service(
    repository: UserAccountRepositoryContract,
    logger: LoggerContract,
) -> UpdateAccountServiceContract:
    """Get update account service instance"""
    from app.context.user_account.domain.services.update_account_service import (
        UpdateAccountService,
    )

    return UpdateAccountService(repository, logger)
