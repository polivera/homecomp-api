from app.context.credit_card.application.contracts import (
    FindCreditCardByIdHandlerContract,
)
from app.context.credit_card.application.dto import CreditCardResponseDTO
from app.context.credit_card.application.queries import FindCreditCardByIdQuery
from app.context.credit_card.domain.contracts.infrastructure import (
    CreditCardRepositoryContract,
)
from app.context.credit_card.domain.value_objects import CreditCardID
from app.shared.domain.contracts import LoggerContract


class FindCreditCardByIdHandler(FindCreditCardByIdHandlerContract):
    """Handler for find credit card by ID query"""

    def __init__(self, repository: CreditCardRepositoryContract, logger: LoggerContract):
        self._repository = repository
        self._logger = logger

    async def handle(self, query: FindCreditCardByIdQuery) -> CreditCardResponseDTO | None:
        """Execute the find credit card by ID query"""

        self._logger.debug(
            "Finding credit card by ID",
            credit_card_id=query.credit_card_id,
            user_id=query.user_id,
        )

        # Convert query primitives to value objects and find card for user
        from app.context.credit_card.domain.value_objects import CreditCardUserID

        card_dto = await self._repository.find_user_credit_card_by_id(
            user_id=CreditCardUserID(query.user_id),
            card_id=CreditCardID(query.credit_card_id),
        )

        if not card_dto:
            self._logger.debug(
                "Credit card not found",
                credit_card_id=query.credit_card_id,
                user_id=query.user_id,
            )
            return None

        return CreditCardResponseDTO.from_domain_dto(card_dto)
