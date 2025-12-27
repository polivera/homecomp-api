from app.context.credit_card.application.contracts.find_credit_cards_by_user_handler_contract import (
    FindCreditCardsByUserHandlerContract,
)
from app.context.credit_card.application.queries.find_credit_cards_by_user_query import (
    FindCreditCardsByUserQuery,
)
from app.context.credit_card.application.dto.credit_card_response_dto import (
    CreditCardResponseDTO,
)
from app.context.credit_card.domain.contracts.infrastructure.credit_card_repository_contract import (
    CreditCardRepositoryContract,
)


class FindCreditCardsByUserHandler(FindCreditCardsByUserHandlerContract):
    """Handler for find credit cards by user query"""

    def __init__(self, repository: CreditCardRepositoryContract):
        self._repository = repository

    async def handle(
        self, query: FindCreditCardsByUserQuery
    ) -> list[CreditCardResponseDTO]:
        """Execute the find credit cards by user query"""

        card_dtos = await self._repository.find_credit_cards_by_user(
            user_id=query.user_id
        )

        return [CreditCardResponseDTO.from_domain_dto(dto) for dto in card_dtos]
