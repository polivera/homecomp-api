from typing import Optional

from app.context.credit_card.application.contracts.find_credit_card_by_id_handler_contract import (
    FindCreditCardByIdHandlerContract,
)
from app.context.credit_card.application.queries.find_credit_card_by_id_query import (
    FindCreditCardByIdQuery,
)
from app.context.credit_card.application.dto.credit_card_response_dto import (
    CreditCardResponseDTO,
)
from app.context.credit_card.domain.contracts.infrastructure.credit_card_repository_contract import (
    CreditCardRepositoryContract,
)


class FindCreditCardByIdHandler(FindCreditCardByIdHandlerContract):
    """Handler for find credit card by ID query"""

    def __init__(self, repository: CreditCardRepositoryContract):
        self._repository = repository

    async def handle(
        self, query: FindCreditCardByIdQuery
    ) -> Optional[CreditCardResponseDTO]:
        """Execute the find credit card by ID query"""

        card_dto = await self._repository.find_credit_card(
            card_id=query.credit_card_id
        )

        if not card_dto:
            return None

        # Verify ownership
        if card_dto.user_id.value != query.user_id.value:
            return None

        return CreditCardResponseDTO.from_domain_dto(card_dto)
