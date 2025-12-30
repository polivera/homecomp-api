from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.context.credit_card.application.commands import DeleteCreditCardCommand
from app.context.credit_card.application.contracts import (
    DeleteCreditCardHandlerContract,
)
from app.context.credit_card.application.dto import DeleteCreditCardErrorCode
from app.context.credit_card.infrastructure.dependencies import (
    get_delete_credit_card_handler,
)
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter(prefix="/cards")


@router.delete("/{credit_card_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_credit_card(
    credit_card_id: int,
    handler: Annotated[DeleteCreditCardHandlerContract, Depends(get_delete_credit_card_handler)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    """Delete a credit card (soft delete)"""
    command = DeleteCreditCardCommand(
        credit_card_id=credit_card_id,
        user_id=user_id,
    )

    result = await handler.handle(command)

    # Check for errors and map error codes to HTTP status codes
    if result.error_code:
        status_code_map = {
            DeleteCreditCardErrorCode.NOT_FOUND: 404,  # Not Found
            DeleteCreditCardErrorCode.UNEXPECTED_ERROR: 500,  # Internal Server Error
        }
        status_code = status_code_map.get(result.error_code, 500)
        raise HTTPException(status_code=status_code, detail=result.error_message)

    return None
