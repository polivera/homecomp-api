from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.context.credit_card.application.commands import DeleteCreditCardCommand
from app.context.credit_card.application.dto import DeleteCreditCardErrorCode
from app.shared.infrastructure.container import ApplicationContainer, get_fastapi_app_container
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter(prefix="/cards")


@router.delete("/{credit_card_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_credit_card(
    credit_card_id: int,
    app_container: Annotated[ApplicationContainer, Depends(get_fastapi_app_container)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    """Delete a credit card (soft delete)"""
    logger = app_container.logger
    handler = app_container.get_delete_credit_card_handler()

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
