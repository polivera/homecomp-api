from app.context.credit_card.application.contracts import (
    FindCreditCardsByUserHandlerContract,
)
from app.context.credit_card.application.dto import CreditCardResponseDTO
from app.context.credit_card.application.queries import FindCreditCardsByUserQuery
from app.context.credit_card.domain.contracts.infrastructure.credit_card_repository_contract import (
    CreditCardRepositoryContract,
)
from app.context.credit_card.domain.value_objects import CreditCardUserID
from app.shared.domain.contracts import LoggerContract


class FindCreditCardsByUserHandler(FindCreditCardsByUserHandlerContract):
    """Handler for find credit cards by user query"""

    def __init__(self, repository: CreditCardRepositoryContract, logger: LoggerContract):
        self._repository = repository
        self._logger = logger

    async def handle(self, query: FindCreditCardsByUserQuery) -> list[CreditCardResponseDTO]:
        """Execute the find credit cards by user query"""

        self._logger.debug("Finding credit cards for user", user_id=query.user_id)

        # Convert query primitive to value object
        card_dtos = await self._repository.find_user_credit_cards(user_id=CreditCardUserID(query.user_id))

        return [CreditCardResponseDTO.from_domain_dto(dto) for dto in card_dtos or []]
