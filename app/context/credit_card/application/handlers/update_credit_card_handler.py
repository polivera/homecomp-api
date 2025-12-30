from app.context.credit_card.application.commands import UpdateCreditCardCommand
from app.context.credit_card.application.contracts import (
    UpdateCreditCardHandlerContract,
)
from app.context.credit_card.application.dto import (
    UpdateCreditCardErrorCode,
    UpdateCreditCardResult,
)
from app.context.credit_card.domain.contracts.services.update_credit_card_service_contract import (
    UpdateCreditCardServiceContract,
)
from app.context.credit_card.domain.exceptions import (
    CreditCardMapperError,
    CreditCardNameAlreadyExistError,
    CreditCardNotFoundError,
)
from app.context.credit_card.domain.value_objects import (
    CardLimit,
    CardUsed,
    CreditCardCurrency,
    CreditCardID,
    CreditCardName,
    CreditCardUserID,
)
from app.shared.domain.contracts import LoggerContract


class UpdateCreditCardHandler(UpdateCreditCardHandlerContract):
    """Handler for update credit card command"""

    def __init__(self, service: UpdateCreditCardServiceContract, logger: LoggerContract):
        self._service = service
        self._logger = logger

    async def handle(self, command: UpdateCreditCardCommand) -> UpdateCreditCardResult:
        """Execute the update credit card command"""

        self._logger.debug(
            "Handling update credit card command",
            credit_card_id=command.credit_card_id,
            user_id=command.user_id,
            name=command.name,
        )

        try:
            # Convert command primitives to value objects
            credit_card_id = CreditCardID(command.credit_card_id)
            user_id = CreditCardUserID(command.user_id)
            name = CreditCardName(command.name) if command.name else None
            currency = CreditCardCurrency(command.currency) if command.currency else None
            limit = CardLimit.from_float(command.limit) if command.limit is not None else None
            used = CardUsed.from_float(command.used) if command.used is not None else None

            # Call service with value objects
            updated_dto = await self._service.update_credit_card(
                credit_card_id=credit_card_id,
                user_id=user_id,
                currency=currency,
                name=name,
                limit=limit,
                used=used,
            )

            # Return success result with updated data
            return UpdateCreditCardResult(
                credit_card_id=updated_dto.credit_card_id.value,
                credit_card_name=updated_dto.name.value,
            )

        # Catch specific domain exceptions and return error codes
        except CreditCardNotFoundError:
            self._logger.debug(
                "Credit card not found", credit_card_id=command.credit_card_id, user_id=command.user_id
            )
            return UpdateCreditCardResult(
                error_code=UpdateCreditCardErrorCode.NOT_FOUND,
                error_message="Credit card not found",
            )
        except CreditCardNameAlreadyExistError:
            self._logger.debug(
                "Credit card name already exists",
                user_id=command.user_id,
                name=command.name,
            )
            return UpdateCreditCardResult(
                error_code=UpdateCreditCardErrorCode.NAME_ALREADY_EXISTS,
                error_message="Credit card name already exists",
            )
        except CreditCardMapperError:
            self._logger.error(
                "Credit card mapper error",
                credit_card_id=command.credit_card_id,
                user_id=command.user_id,
            )
            return UpdateCreditCardResult(
                error_code=UpdateCreditCardErrorCode.MAPPER_ERROR,
                error_message="Error mapping model to dto",
            )

        # Always catch generic Exception as final fallback
        except Exception as e:
            self._logger.error(
                "Unexpected error updating credit card",
                credit_card_id=command.credit_card_id,
                user_id=command.user_id,
                error=str(e),
            )
            return UpdateCreditCardResult(
                error_code=UpdateCreditCardErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error",
            )
