from app.context.credit_card.domain.contracts.infrastructure.credit_card_repository_contract import (
    CreditCardRepositoryContract,
)
from app.context.credit_card.domain.contracts.services.create_credit_card_service_contract import (
    CreateCreditCardServiceContract,
)
from app.context.credit_card.domain.dto.credit_card_dto import CreditCardDTO
from app.context.credit_card.domain.value_objects import (
    CreditCardAccountID,
    CreditCardCurrency,
    CreditCardUserID,
)
from app.context.credit_card.domain.value_objects.card_limit import CardLimit
from app.context.credit_card.domain.value_objects.credit_card_name import (
    CreditCardName,
)
from app.shared.domain.contracts import LoggerContract


class CreateCreditCardService(CreateCreditCardServiceContract):
    """Service for creating credit cards"""

    def __init__(self, card_repository: CreditCardRepositoryContract, logger: LoggerContract):
        self._card_repository = card_repository
        self._logger = logger

    async def create_credit_card(
        self,
        user_id: CreditCardUserID,
        account_id: CreditCardAccountID,
        name: CreditCardName,
        currency: CreditCardCurrency,
        limit: CardLimit,
    ) -> CreditCardDTO:
        """Create a new credit card with validation"""

        self._logger.debug(
            "Creating credit card",
            user_id=user_id.value,
            account_id=account_id.value,
            name=name.value,
            currency=currency.value,
            limit=float(limit.value),
        )

        card_dto = CreditCardDTO(
            user_id=user_id,
            account_id=account_id,
            name=name,
            currency=currency,
            limit=limit,
        )

        # Save and return the new credit card
        return await self._card_repository.save_credit_card(card_dto)
