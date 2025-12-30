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
from app.shared.domain.contracts import LoggerContract


class CreateCreditCardHandler(CreateCreditCardHandlerContract):
    """Handler for create credit card command"""

    def __init__(self, service: CreateCreditCardServiceContract, logger: LoggerContract):
        self._service = service
        self._logger = logger

    async def handle(self, command: CreateCreditCardCommand) -> CreateCreditCardResult:
        """Execute the create credit card command"""

        self._logger.debug(
            "Handling create credit card command",
            user_id=command.user_id,
            account_id=command.account_id,
            name=command.name,
        )

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
                self._logger.error(
                    "Credit card created but ID is None",
                    user_id=command.user_id,
                    account_id=command.account_id,
                )
                return CreateCreditCardResult(
                    error_code=CreateCreditCardErrorCode.UNEXPECTED_ERROR,
                    error_message="Error creating credit card",
                )

            # Return success result
            return CreateCreditCardResult(credit_card_id=card_dto.credit_card_id.value)

        # Catch specific domain exceptions and return error codes
        except CreditCardNameAlreadyExistError:
            self._logger.debug(
                "Credit card name already exists", user_id=command.user_id, name=command.name
            )
            return CreateCreditCardResult(
                error_code=CreateCreditCardErrorCode.NAME_ALREADY_EXISTS,
                error_message="Credit card name already exists",
            )
        except CreditCardMapperError:
            self._logger.error("Credit card mapper error", user_id=command.user_id)
            return CreateCreditCardResult(
                error_code=CreateCreditCardErrorCode.MAPPER_ERROR,
                error_message="Error mapping model to dto",
            )

        # Always catch generic Exception as final fallback
        except Exception as e:
            self._logger.error(
                "Unexpected error creating credit card", user_id=command.user_id, error=str(e)
            )
            return CreateCreditCardResult(
                error_code=CreateCreditCardErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error",
            )
