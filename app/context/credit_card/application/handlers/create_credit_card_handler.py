from app.context.credit_card.application.commands import CreateCreditCardCommand
from app.context.credit_card.application.contracts import (
    CreateCreditCardHandlerContract,
)
from app.context.credit_card.application.dto import (
    CreateCreditCardErrorCode,
    CreateCreditCardResult,
)
from app.context.credit_card.domain.contracts.services.create_credit_card_service_contract import (
    CreateCreditCardServiceContract,
)
from app.context.credit_card.domain.exceptions import (
    CreditCardMapperError,
    CreditCardNameAlreadyExistError,
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

        try:
            # Convert command primitives to value objects
            card_dto = await self._service.create_credit_card(
                user_id=CreditCardUserID(command.user_id),
                account_id=CreditCardAccountID(command.account_id),
                name=CreditCardName(command.name),
                currency=CreditCardCurrency(command.currency),
                limit=CardLimit.from_float(command.limit),
            )

            # Validate operation succeeded
            if card_dto.credit_card_id is None:
                return CreateCreditCardResult(
                    error_code=CreateCreditCardErrorCode.UNEXPECTED_ERROR,
                    error_message="Error creating credit card",
                )

            # Return success result
            return CreateCreditCardResult(credit_card_id=card_dto.credit_card_id.value)

        # Catch specific domain exceptions and return error codes
        except CreditCardNameAlreadyExistError:
            return CreateCreditCardResult(
                error_code=CreateCreditCardErrorCode.NAME_ALREADY_EXISTS,
                error_message="Credit card name already exists",
            )
        except CreditCardMapperError:
            return CreateCreditCardResult(
                error_code=CreateCreditCardErrorCode.MAPPER_ERROR,
                error_message="Error mapping model to dto",
            )

        # Always catch generic Exception as final fallback
        except Exception:
            return CreateCreditCardResult(
                error_code=CreateCreditCardErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error",
            )
