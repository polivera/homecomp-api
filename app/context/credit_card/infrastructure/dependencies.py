from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.infrastructure.database import get_db
from app.context.credit_card.domain.contracts.infrastructure.credit_card_repository_contract import (
    CreditCardRepositoryContract,
)
from app.context.credit_card.domain.contracts.services.create_credit_card_service_contract import (
    CreateCreditCardServiceContract,
)
from app.context.credit_card.domain.contracts.services.update_credit_card_service_contract import (
    UpdateCreditCardServiceContract,
)
from app.context.credit_card.application.contracts.create_credit_card_handler_contract import (
    CreateCreditCardHandlerContract,
)
from app.context.credit_card.application.contracts.update_credit_card_handler_contract import (
    UpdateCreditCardHandlerContract,
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


# ─────────────────────────────────────────────────────────────────
# REPOSITORY
# ─────────────────────────────────────────────────────────────────


def get_credit_card_repository(
    db: AsyncSession = Depends(get_db),
) -> CreditCardRepositoryContract:
    """CreditCardRepository dependency injection"""
    from app.context.credit_card.infrastructure.repositories.credit_card_repository import (
        CreditCardRepository,
    )

    return CreditCardRepository(db)


# ─────────────────────────────────────────────────────────────────
# COMMAND HANDLERS (Write operations)
# ─────────────────────────────────────────────────────────────────


def get_create_credit_card_service(
    card_repository: CreditCardRepositoryContract = Depends(get_credit_card_repository),
) -> CreateCreditCardServiceContract:
    """CreateCreditCardService dependency injection"""
    from app.context.credit_card.domain.services.create_credit_card_service import (
        CreateCreditCardService,
    )

    return CreateCreditCardService(card_repository)


def get_create_credit_card_handler(
    service: CreateCreditCardServiceContract = Depends(get_create_credit_card_service),
) -> CreateCreditCardHandlerContract:
    """CreateCreditCardHandler dependency injection"""
    from app.context.credit_card.application.handlers.create_credit_card_handler import (
        CreateCreditCardHandler,
    )

    return CreateCreditCardHandler(service)


def get_update_credit_card_service(
    repository: CreditCardRepositoryContract = Depends(get_credit_card_repository),
) -> UpdateCreditCardServiceContract:
    """UpdateCreditCardService dependency injection"""
    from app.context.credit_card.domain.services.update_credit_card_service import (
        UpdateCreditCardService,
    )

    return UpdateCreditCardService(repository)


def get_update_credit_card_handler(
    service: UpdateCreditCardServiceContract = Depends(get_update_credit_card_service),
) -> UpdateCreditCardHandlerContract:
    """UpdateCreditCardHandler dependency injection"""
    from app.context.credit_card.application.handlers.update_credit_card_handler import (
        UpdateCreditCardHandler,
    )

    return UpdateCreditCardHandler(service)


def get_delete_credit_card_handler(
    repository: CreditCardRepositoryContract = Depends(get_credit_card_repository),
) -> DeleteCreditCardHandlerContract:
    """DeleteCreditCardHandler dependency injection"""
    from app.context.credit_card.application.handlers.delete_credit_card_handler import (
        DeleteCreditCardHandler,
    )

    return DeleteCreditCardHandler(repository)


# ─────────────────────────────────────────────────────────────────
# QUERY HANDLERS (Read operations)
# ─────────────────────────────────────────────────────────────────


def get_find_credit_card_by_id_handler(
    repository: CreditCardRepositoryContract = Depends(get_credit_card_repository),
) -> FindCreditCardByIdHandlerContract:
    """FindCreditCardByIdHandler dependency injection"""
    from app.context.credit_card.application.handlers.find_credit_card_by_id_handler import (
        FindCreditCardByIdHandler,
    )

    return FindCreditCardByIdHandler(repository)


def get_find_credit_cards_by_user_handler(
    repository: CreditCardRepositoryContract = Depends(get_credit_card_repository),
) -> FindCreditCardsByUserHandlerContract:
    """FindCreditCardsByUserHandler dependency injection"""
    from app.context.credit_card.application.handlers.find_credit_cards_by_user_handler import (
        FindCreditCardsByUserHandler,
    )

    return FindCreditCardsByUserHandler(repository)
