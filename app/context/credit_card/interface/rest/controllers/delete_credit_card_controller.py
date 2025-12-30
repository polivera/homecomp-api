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
from app.shared.domain.contracts import LoggerContract
from app.shared.infrastructure.dependencies import get_logger
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter(prefix="/cards")


@router.delete("/{credit_card_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_credit_card(
    credit_card_id: int,
    handler: Annotated[DeleteCreditCardHandlerContract, Depends(get_delete_credit_card_handler)],
    user_id: Annotated[int, Depends(get_current_user_id)],
    logger: Annotated[LoggerContract, Depends(get_logger)],
):
    """Delete a credit card (soft delete)"""
    logger.info("Delete credit card request", user_id=user_id, credit_card_id=credit_card_id)

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

        if status_code == 404:
            logger.warning("Delete credit card failed - not found", user_id=user_id, credit_card_id=credit_card_id)
        elif status_code == 500:
            logger.error(
                "Delete credit card failed - server error",
                user_id=user_id,
                credit_card_id=credit_card_id,
                error_code=result.error_code.value,
            )

        raise HTTPException(status_code=status_code, detail=result.error_message)

    logger.info("Credit card deleted successfully", user_id=user_id, credit_card_id=credit_card_id)

    return None
