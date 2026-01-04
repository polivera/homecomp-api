from sqlalchemy.ext.asyncio import AsyncSession

from app.context.credit_card.application.contracts.create_credit_card_handler_contract import (
    CreateCreditCardHandlerContract,
)
from app.context.credit_card.application.contracts.delete_credit_card_handler_contract import (
    DeleteCreditCardHandlerContract,
)
from app.context.credit_card.application.contracts.find_credit_card_by_id_handler_contract import (
    FindCreditCardByIdHandlerContract,
)
from app.context.credit_card.application.contracts.find_credit_cards_by_user_handler_contract import (
    FindCreditCardsByUserHandlerContract,
)
from app.context.credit_card.application.contracts.update_credit_card_handler_contract import (
    UpdateCreditCardHandlerContract,
)
from app.context.credit_card.domain.contracts.infrastructure.credit_card_repository_contract import (
    CreditCardRepositoryContract,
)
from app.context.credit_card.domain.contracts.services.create_credit_card_service_contract import (
    CreateCreditCardServiceContract,
)
from app.context.credit_card.domain.contracts.services.update_credit_card_service_contract import (
    UpdateCreditCardServiceContract,
)
from app.shared.domain.contracts import LoggerContract


# ─────────────────────────────────────────────────────────────────
# COMMAND HANDLERS (Write operations)
# ─────────────────────────────────────────────────────────────────


def create_credit_card_handler_factory(
    db: AsyncSession,
    logger: LoggerContract,
) -> CreateCreditCardHandlerContract:
    """Factory for CreateCreditCardHandler with all dependencies"""
    from app.context.credit_card.application.handlers.create_credit_card_handler import (
        CreateCreditCardHandler,
    )

    service = _get_create_credit_card_service(_get_credit_card_repository(db), logger)
    return CreateCreditCardHandler(service, logger)


def update_credit_card_handler_factory(
    db: AsyncSession,
    logger: LoggerContract,
) -> UpdateCreditCardHandlerContract:
    """Factory for UpdateCreditCardHandler with all dependencies"""
    from app.context.credit_card.application.handlers.update_credit_card_handler import (
        UpdateCreditCardHandler,
    )

    service = _get_update_credit_card_service(_get_credit_card_repository(db), logger)
    return UpdateCreditCardHandler(service, logger)


def delete_credit_card_handler_factory(
    db: AsyncSession,
    logger: LoggerContract,
) -> DeleteCreditCardHandlerContract:
    """Factory for DeleteCreditCardHandler with all dependencies"""
    from app.context.credit_card.application.handlers.delete_credit_card_handler import (
        DeleteCreditCardHandler,
    )

    repository = _get_credit_card_repository(db)
    return DeleteCreditCardHandler(repository, logger)


# ─────────────────────────────────────────────────────────────────
# QUERY HANDLERS (Read operations)
# ─────────────────────────────────────────────────────────────────


def find_credit_card_by_id_handler_factory(
    db: AsyncSession,
    logger: LoggerContract,
) -> FindCreditCardByIdHandlerContract:
    """Factory for FindCreditCardByIdHandler with all dependencies"""
    from app.context.credit_card.application.handlers.find_credit_card_by_id_handler import (
        FindCreditCardByIdHandler,
    )

    repository = _get_credit_card_repository(db)
    return FindCreditCardByIdHandler(repository, logger)


def find_credit_cards_by_user_handler_factory(
    db: AsyncSession,
    logger: LoggerContract,
) -> FindCreditCardsByUserHandlerContract:
    """Factory for FindCreditCardsByUserHandler with all dependencies"""
    from app.context.credit_card.application.handlers.find_credit_cards_by_user_handler import (
        FindCreditCardsByUserHandler,
    )

    repository = _get_credit_card_repository(db)
    return FindCreditCardsByUserHandler(repository, logger)


# ─────────────────────────────────────────────────────────────────
# Private helper functions
# ─────────────────────────────────────────────────────────────────


def _get_credit_card_repository(db: AsyncSession) -> CreditCardRepositoryContract:
    """Get credit card repository instance"""
    from app.context.credit_card.infrastructure.repositories.credit_card_repository import (
        CreditCardRepository,
    )

    return CreditCardRepository(db)


def _get_create_credit_card_service(
    repository: CreditCardRepositoryContract,
    logger: LoggerContract,
) -> CreateCreditCardServiceContract:
    """Get create credit card service instance"""
    from app.context.credit_card.domain.services.create_credit_card_service import (
        CreateCreditCardService,
    )

    return CreateCreditCardService(repository, logger)


def _get_update_credit_card_service(
    repository: CreditCardRepositoryContract,
    logger: LoggerContract,
) -> UpdateCreditCardServiceContract:
    """Get update credit card service instance"""
    from app.context.credit_card.domain.services.update_credit_card_service import (
        UpdateCreditCardService,
    )

    return UpdateCreditCardService(repository, logger)
