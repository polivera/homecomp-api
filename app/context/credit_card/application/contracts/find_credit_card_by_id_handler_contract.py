from abc import ABC, abstractmethod
from typing import Optional

from app.context.credit_card.application.queries.find_credit_card_by_id_query import (
    FindCreditCardByIdQuery,
)
from app.context.credit_card.application.dto.credit_card_response_dto import (
    CreditCardResponseDTO,
)


class FindCreditCardByIdHandlerContract(ABC):
    """Contract for find credit card by ID query handler"""

    @abstractmethod
    async def handle(
        self, query: FindCreditCardByIdQuery
    ) -> Optional[CreditCardResponseDTO]:
        """Handle the find credit card by ID query"""
        pass
