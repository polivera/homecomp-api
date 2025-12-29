from app.context.credit_card.application.contracts import (
    FindCreditCardByIdHandlerContract,
)
from app.context.credit_card.application.dto import CreditCardResponseDTO
from app.context.credit_card.application.queries import FindCreditCardByIdQuery
from app.context.credit_card.domain.contracts.infrastructure import (
    CreditCardRepositoryContract,
)
from app.context.credit_card.domain.value_objects import CreditCardID


class FindCreditCardByIdHandler(FindCreditCardByIdHandlerContract):
    """Handler for find credit card by ID query"""

    def __init__(self, repository: CreditCardRepositoryContract):
        self._repository = repository

    async def handle(self, query: FindCreditCardByIdQuery) -> CreditCardResponseDTO | None:
        """Execute the find credit card by ID query"""

        # Convert query primitives to value objects and find card for user
        from app.context.credit_card.domain.value_objects import CreditCardUserID

        card_dto = await self._repository.find_user_credit_card_by_id(
            user_id=CreditCardUserID(query.user_id),
            card_id=CreditCardID(query.credit_card_id),
        )

        if not card_dto:
            return None

        return CreditCardResponseDTO.from_domain_dto(card_dto)
