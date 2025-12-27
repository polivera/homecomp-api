from app.context.credit_card.application.commands.delete_credit_card_command import (
    DeleteCreditCardCommand,
)
from app.context.credit_card.application.contracts.delete_credit_card_handler_contract import (
    DeleteCreditCardHandlerContract,
)
from app.context.credit_card.domain.contracts.infrastructure.credit_card_repository_contract import (
    CreditCardRepositoryContract,
)


class DeleteCreditCardHandler(DeleteCreditCardHandlerContract):
    """Handler for delete credit card command"""

    def __init__(self, repository: CreditCardRepositoryContract):
        self._repository = repository

    async def handle(self, command: DeleteCreditCardCommand) -> bool:
        """Execute the delete credit card command"""

        return await self._repository.delete_credit_card(
            card_id=command.credit_card_id,
            user_id=command.user_id,
        )
