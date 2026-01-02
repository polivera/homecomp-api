from abc import ABC, abstractmethod

from app.context.credit_card.application.dto.credit_card_response_dto import (
    CreditCardResponseDTO,
)
from app.context.credit_card.application.queries.find_credit_cards_by_user_query import (
    FindCreditCardsByUserQuery,
)


class FindCreditCardsByUserHandlerContract(ABC):
    """Contract for find credit cards by user query handler"""

    @abstractmethod
    async def handle(self, query: FindCreditCardsByUserQuery) -> list[CreditCardResponseDTO]:
        """Handle the find credit cards by user query"""
        pass
