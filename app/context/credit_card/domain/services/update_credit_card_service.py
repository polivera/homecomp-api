from app.context.credit_card.domain.contracts.infrastructure.credit_card_repository_contract import (
    CreditCardRepositoryContract,
)
from app.context.credit_card.domain.contracts.services.update_credit_card_service_contract import (
    UpdateCreditCardServiceContract,
)
from app.context.credit_card.domain.dto.credit_card_dto import CreditCardDTO
from app.context.credit_card.domain.exceptions import (
    CreditCardNameAlreadyExistError,
    CreditCardNotFoundError,
    CreditCardUnauthorizedAccessError,
    CreditCardUsedExceedsLimitError,
)
from app.context.credit_card.domain.value_objects import (
    CreditCardCurrency,
    CreditCardUserID,
)
from app.context.credit_card.domain.value_objects.card_limit import CardLimit
from app.context.credit_card.domain.value_objects.card_used import CardUsed
from app.context.credit_card.domain.value_objects.credit_card_id import CreditCardID
from app.context.credit_card.domain.value_objects.credit_card_name import (
    CreditCardName,
)
from app.shared.domain.contracts import LoggerContract


class UpdateCreditCardService(UpdateCreditCardServiceContract):
    """Service for updating credit cards"""

    def __init__(self, repository: CreditCardRepositoryContract, logger: LoggerContract):
        self._repository = repository
        self._logger = logger

    async def update_credit_card(
        self,
        credit_card_id: CreditCardID,
        user_id: CreditCardUserID,
        name: CreditCardName | None = None,
        limit: CardLimit | None = None,
        used: CardUsed | None = None,
        currency: CreditCardCurrency | None = None,
    ) -> CreditCardDTO:
        """Update an existing credit card with validation"""

        self._logger.debug(
            "Updating credit card",
            credit_card_id=credit_card_id.value,
            user_id=user_id.value,
            name=name.value if name else None,
            limit=float(limit.value) if limit else None,
            used=float(used.value) if used else None,
        )

        # Find the existing card
        existing_card = await self._repository.find_credit_card(card_id=credit_card_id)

        if not existing_card:
            self._logger.warning(
                "Credit card not found", credit_card_id=credit_card_id.value, user_id=user_id.value
            )
            raise CreditCardNotFoundError(f"Credit card with ID {credit_card_id.value} not found")

        # Verify ownership
        if existing_card.user_id.value != user_id.value:
            self._logger.warning(
                "Unauthorized credit card access attempt",
                credit_card_id=credit_card_id.value,
                user_id=user_id.value,
                owner_id=existing_card.user_id.value,
            )
            raise CreditCardUnauthorizedAccessError(
                f"User {user_id.value} is not authorized to update credit card {credit_card_id.value}"
            )

        # If name is being changed, check for duplicates
        if name and name.value != existing_card.name.value:
            duplicate_card = await self._repository.find_credit_card(user_id=user_id, name=name)
            if duplicate_card:
                self._logger.warning(
                    "Credit card name already exists",
                    user_id=user_id.value,
                    name=name.value,
                    existing_card_id=duplicate_card.credit_card_id.value
                    if duplicate_card.credit_card_id
                    else None,
                )
                raise CreditCardNameAlreadyExistError(
                    f"Credit card with name '{name.value}' already exists for this user"
                )

        # Build updated card DTO with new values or existing ones
        updated_name = name if name else existing_card.name
        updated_limit = limit if limit else existing_card.limit
        updated_used = used if used is not None else existing_card.used

        # Business rule: ensure used <= limit
        if updated_used.value > updated_limit.value:
            self._logger.warning(
                "Credit card used amount exceeds limit",
                credit_card_id=credit_card_id.value,
                user_id=user_id.value,
                used=float(updated_used.value),
                limit=float(updated_limit.value),
            )
            raise CreditCardUsedExceedsLimitError(
                f"Used amount ({updated_used.value}) cannot exceed limit ({updated_limit.value})"
            )

        # Create updated DTO
        updated_card = CreditCardDTO(
            credit_card_id=existing_card.credit_card_id,
            user_id=existing_card.user_id,
            account_id=existing_card.account_id,
            name=updated_name,
            currency=existing_card.currency,
            limit=updated_limit,
            used=updated_used,
        )

        # Save and return
        return await self._repository.update_credit_card(updated_card)
