from typing import Optional

from app.context.credit_card.application.contracts import (
    FindCreditCardByIdHandlerContract,
)
from app.context.credit_card.application.dto import CreditCardResponseDTO
from app.context.credit_card.application.queries import FindCreditCardByIdQuery
from app.context.credit_card.domain.contracts.infrastructure.credit_card_repository_contract import (
    CreditCardRepositoryContract,
)
from app.context.credit_card.domain.value_objects import CreditCardID, CreditCardUserID


class FindCreditCardByIdHandler(FindCreditCardByIdHandlerContract):
    """Handler for find credit card by ID query"""

    def __init__(self, repository: CreditCardRepositoryContract):
        self._repository = repository

    async def handle(
        self, query: FindCreditCardByIdQuery
    ) -> Optional[CreditCardResponseDTO]:
        """Execute the find credit card by ID query"""

        # Convert query primitives to value objects
        card_dto = await self._repository.find_credit_card(
            card_id=CreditCardID(query.credit_card_id)
        )

        if not card_dto:
            return None

        # Verify ownership (query uses primitive, card_dto has value object)
        if card_dto.user_id.value != query.user_id:
            return None

        return CreditCardResponseDTO.from_domain_dto(card_dto)
