from app.context.credit_card.application.commands.create_credit_card_command import (
    CreateCreditCardCommand,
)
from app.context.credit_card.application.contracts.create_credit_card_handler_contract import (
    CreateCreditCardHandlerContract,
)
from app.context.credit_card.application.dto.create_credit_card_result import (
    CreateCreditCardResult,
)
from app.context.credit_card.domain.contracts.services.create_credit_card_service_contract import (
    CreateCreditCardServiceContract,
)
from app.context.credit_card.domain.value_objects import (
    CardLimit,
    CreditCardAccountID,
    CreditCardCurrency,
    CreditCardName,
    CreditCardUserID,
)


class CreateCreditCardHandler(CreateCreditCardHandlerContract):
    """Handler for create credit card command"""

    def __init__(self, service: CreateCreditCardServiceContract):
        self._service = service

    async def handle(self, command: CreateCreditCardCommand) -> CreateCreditCardResult:
        """Execute the create credit card command"""

        card_dto = await self._service.create_credit_card(
            user_id=CreditCardUserID(command.user_id),
            account_id=CreditCardAccountID(command.account_id),
            name=CreditCardName(command.name),
            currency=CreditCardCurrency(command.currency),
            limit=CardLimit.from_float(command.limit),
        )

        if card_dto.credit_card_id is None:
            return CreateCreditCardResult(error="Error creating credit card")

        return CreateCreditCardResult(credit_card_id=card_dto.credit_card_id.value)
