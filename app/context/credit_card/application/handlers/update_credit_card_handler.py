from app.context.credit_card.application.commands.update_credit_card_command import (
    UpdateCreditCardCommand,
)
from app.context.credit_card.application.contracts.update_credit_card_handler_contract import (
    UpdateCreditCardHandlerContract,
)
from app.context.credit_card.application.dto.update_credit_card_result import (
    UpdateCreditCardResult,
)
from app.context.credit_card.domain.contracts.services.update_credit_card_service_contract import (
    UpdateCreditCardServiceContract,
)


class UpdateCreditCardHandler(UpdateCreditCardHandlerContract):
    """Handler for update credit card command"""

    def __init__(self, service: UpdateCreditCardServiceContract):
        self._service = service

    async def handle(
        self, command: UpdateCreditCardCommand
    ) -> UpdateCreditCardResult:
        """Execute the update credit card command"""

        try:
            await self._service.update_credit_card(
                credit_card_id=command.credit_card_id,
                user_id=command.user_id,
                name=command.name,
                limit=command.limit,
                used=command.used,
            )

            return UpdateCreditCardResult(success=True)

        except ValueError as e:
            return UpdateCreditCardResult(success=False, error=str(e))
