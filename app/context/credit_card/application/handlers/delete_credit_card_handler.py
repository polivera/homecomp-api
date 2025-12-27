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


class DeleteCreditCardHandler(DeleteCreditCardHandlerContract):
    """Handler for delete credit card command"""

    def __init__(self, repository: CreditCardRepositoryContract):
        self._repository = repository

    async def handle(self, command: DeleteCreditCardCommand) -> DeleteCreditCardResult:
        """Execute the delete credit card command"""

        try:
            # Convert command primitives to value objects
            success = await self._repository.delete_credit_card(
                card_id=CreditCardID(command.credit_card_id),
                user_id=CreditCardUserID(command.user_id),
            )

            if not success:
                return DeleteCreditCardResult(
                    error_code=DeleteCreditCardErrorCode.NOT_FOUND,
                    error_message="Credit card not found",
                )

            return DeleteCreditCardResult(success=True)

        # Catch specific domain exceptions and return error codes
        except CreditCardNotFoundError:
            return DeleteCreditCardResult(
                error_code=DeleteCreditCardErrorCode.NOT_FOUND,
                error_message="Credit card not found",
            )

        # Always catch generic Exception as final fallback
        except Exception:
            return DeleteCreditCardResult(
                error_code=DeleteCreditCardErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error",
            )
