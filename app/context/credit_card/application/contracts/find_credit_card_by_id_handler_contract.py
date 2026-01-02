from abc import ABC, abstractmethod

from app.context.credit_card.application.dto.credit_card_response_dto import (
    CreditCardResponseDTO,
)
from app.context.credit_card.application.queries.find_credit_card_by_id_query import (
    FindCreditCardByIdQuery,
)


class FindCreditCardByIdHandlerContract(ABC):
    """Contract for find credit card by ID query handler"""

    @abstractmethod
    async def handle(self, query: FindCreditCardByIdQuery) -> CreditCardResponseDTO | None:
        """Handle the find credit card by ID query"""
        pass
