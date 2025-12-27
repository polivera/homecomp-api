from fastapi import APIRouter, Depends, HTTPException, status

from app.context.user.domain.value_objects.user_id import UserID
from app.context.credit_card.application.commands.delete_credit_card_command import (
    DeleteCreditCardCommand,
)
from app.context.credit_card.application.contracts.delete_credit_card_handler_contract import (
    DeleteCreditCardHandlerContract,
)
from app.context.credit_card.domain.value_objects.credit_card_id import CreditCardID
from app.context.credit_card.infrastructure.dependencies import (
    get_delete_credit_card_handler,
)

router = APIRouter(prefix="/cards", tags=["credit-cards"])


@router.delete("/{credit_card_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_credit_card(
    credit_card_id: int,
    handler: DeleteCreditCardHandlerContract = Depends(get_delete_credit_card_handler),
):
    """Delete a credit card (soft delete)"""

    try:
        # Convert to command
        # TODO: user_id from cookie header
        command = DeleteCreditCardCommand(
            credit_card_id=CreditCardID(credit_card_id),
            user_id=UserID(1),
        )

        # Handle the command
        deleted = await handler.handle(command)

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail=f"Credit card with ID {credit_card_id} not found or not owned by user",
            )

        return None

    except ValueError as e:
        # Validation errors
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Unexpected errors
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )
