from app.context.credit_card.application.commands import DeleteCreditCardCommand
from app.context.credit_card.application.contracts import (
    DeleteCreditCardHandlerContract,
)
from app.context.credit_card.application.dto import (
    DeleteCreditCardErrorCode,
    DeleteCreditCardResult,
)
from app.context.credit_card.domain.contracts.infrastructure.credit_card_repository_contract import (
    CreditCardRepositoryContract,
)
from app.context.credit_card.domain.exceptions import CreditCardNotFoundError
from app.context.credit_card.domain.value_objects import CreditCardID, CreditCardUserID
from app.shared.domain.contracts import LoggerContract


class DeleteCreditCardHandler(DeleteCreditCardHandlerContract):
    """Handler for delete credit card command"""

    def __init__(self, repository: CreditCardRepositoryContract, logger: LoggerContract):
        self._repository = repository
        self._logger = logger

    async def handle(self, command: DeleteCreditCardCommand) -> DeleteCreditCardResult:
        """Execute the delete credit card command"""

        self._logger.debug(
            "Handling delete credit card command",
            credit_card_id=command.credit_card_id,
            user_id=command.user_id,
        )

        try:
            # Convert command primitives to value objects
            success = await self._repository.delete_credit_card(
                card_id=CreditCardID(command.credit_card_id),
                user_id=CreditCardUserID(command.user_id),
            )

            if not success:
                self._logger.warning(
                    "Credit card not found for deletion",
                    credit_card_id=command.credit_card_id,
                    user_id=command.user_id,
                )
                return DeleteCreditCardResult(
                    error_code=DeleteCreditCardErrorCode.NOT_FOUND,
                    error_message="Credit card not found",
                )

            return DeleteCreditCardResult(success=True)

        # Catch specific domain exceptions and return error codes
        except CreditCardNotFoundError:
            self._logger.debug("Credit card not found", credit_card_id=command.credit_card_id, user_id=command.user_id)
            return DeleteCreditCardResult(
                error_code=DeleteCreditCardErrorCode.NOT_FOUND,
                error_message="Credit card not found",
            )

        # Always catch generic Exception as final fallback
        except Exception as e:
            self._logger.error(
                "Unexpected error deleting credit card",
                credit_card_id=command.credit_card_id,
                user_id=command.user_id,
                error=str(e),
            )
            return DeleteCreditCardResult(
                error_code=DeleteCreditCardErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error",
            )
