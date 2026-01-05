from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.context.credit_card.application.commands import UpdateCreditCardCommand
from app.context.credit_card.application.dto import UpdateCreditCardErrorCode
from app.context.credit_card.interface.schemas.update_credit_card_response import (
    UpdateCreditCardResponse,
)
from app.context.credit_card.interface.schemas.update_credit_card_schema import (
    UpdateCreditCardRequest,
)
from app.shared.infrastructure.container import ApplicationContainer, get_fastapi_app_container
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter(prefix="/cards")


@router.put("/{credit_card_id}", response_model=UpdateCreditCardResponse)
async def update_credit_card(
    credit_card_id: int,
    request: UpdateCreditCardRequest,
    app_container: Annotated[ApplicationContainer, Depends(get_fastapi_app_container)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    """Update an existing credit card"""
    logger = app_container.logger
    handler = app_container.get_update_credit_card_handler()

    logger.info("Update credit card request", user_id=user_id, credit_card_id=credit_card_id)

    command = UpdateCreditCardCommand(
        credit_card_id=credit_card_id,
        user_id=user_id,
        name=request.name,
        limit=request.limit,
        used=request.used,
    )

    result = await handler.handle(command)

    # Check for errors and map error codes to HTTP status codes
    if result.error_code:
        status_code_map = {
            UpdateCreditCardErrorCode.NOT_FOUND: 404,  # Not Found
            UpdateCreditCardErrorCode.NAME_ALREADY_EXISTS: 409,  # Conflict
            UpdateCreditCardErrorCode.MAPPER_ERROR: 500,  # Internal Server Error
            UpdateCreditCardErrorCode.UNEXPECTED_ERROR: 500,  # Internal Server Error
        }
        status_code = status_code_map.get(result.error_code, 500)

        if status_code == 404:
            logger.warning("Update credit card failed - not found", user_id=user_id, credit_card_id=credit_card_id)
        elif status_code == 409:
            logger.warning("Update credit card failed - name conflict", user_id=user_id, credit_card_id=credit_card_id)
        elif status_code == 500:
            logger.error(
                "Update credit card failed - server error",
                user_id=user_id,
                credit_card_id=credit_card_id,
                error_code=result.error_code.value,
            )

        raise HTTPException(status_code=status_code, detail=result.error_message)

    logger.info("Credit card updated successfully", user_id=user_id, credit_card_id=credit_card_id)

    return UpdateCreditCardResponse(success=True, message="Credit card updated successfully")
