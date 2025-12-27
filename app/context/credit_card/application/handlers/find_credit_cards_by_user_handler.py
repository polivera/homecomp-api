from app.context.credit_card.application.contracts import (
    FindCreditCardsByUserHandlerContract,
)
from app.context.credit_card.application.dto import CreditCardResponseDTO
from app.context.credit_card.application.queries import FindCreditCardsByUserQuery
from app.context.credit_card.domain.contracts.infrastructure.credit_card_repository_contract import (
    CreditCardRepositoryContract,
)
from app.context.credit_card.domain.value_objects import CreditCardUserID


class FindCreditCardsByUserHandler(FindCreditCardsByUserHandlerContract):
    """Handler for find credit cards by user query"""

    def __init__(self, repository: CreditCardRepositoryContract):
        self._repository = repository

    async def handle(
        self, query: FindCreditCardsByUserQuery
    ) -> list[CreditCardResponseDTO]:
        """Execute the find credit cards by user query"""

        # Convert query primitive to value object
        card_dtos = await self._repository.find_credit_cards_by_user(
            user_id=CreditCardUserID(query.user_id)
        )

        return [CreditCardResponseDTO.from_domain_dto(dto) for dto in card_dtos]
