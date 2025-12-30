from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.context.credit_card.application.commands import UpdateCreditCardCommand
from app.context.credit_card.application.contracts import (
    UpdateCreditCardHandlerContract,
)
from app.context.credit_card.application.dto import UpdateCreditCardErrorCode
from app.context.credit_card.infrastructure.dependencies import (
    get_update_credit_card_handler,
)
from app.context.credit_card.interface.schemas.update_credit_card_response import (
    UpdateCreditCardResponse,
)
from app.context.credit_card.interface.schemas.update_credit_card_schema import (
    UpdateCreditCardRequest,
)
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter(prefix="/cards")


@router.put("/{credit_card_id}", response_model=UpdateCreditCardResponse)
async def update_credit_card(
    credit_card_id: int,
    request: UpdateCreditCardRequest,
    handler: Annotated[UpdateCreditCardHandlerContract, Depends(get_update_credit_card_handler)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    """Update an existing credit card"""
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
        raise HTTPException(status_code=status_code, detail=result.error_message)

    return UpdateCreditCardResponse(success=True, message="Credit card updated successfully")
