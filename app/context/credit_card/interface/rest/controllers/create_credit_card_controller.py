from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.context.credit_card.application.commands import CreateCreditCardCommand
from app.context.credit_card.application.contracts import (
    CreateCreditCardHandlerContract,
)
from app.context.credit_card.application.dto import CreateCreditCardErrorCode
from app.context.credit_card.domain.value_objects import CardLimit
from app.context.credit_card.infrastructure.dependencies import (
    get_create_credit_card_handler,
)
from app.context.credit_card.interface.schemas.create_credit_card_response import (
    CreateCreditCardResponse,
)
from app.context.credit_card.interface.schemas.create_credit_card_schema import (
    CreateCreditCardRequest,
)
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter(prefix="/cards", tags=["credit-cards"])


@router.post("", response_model=CreateCreditCardResponse, status_code=201)
async def create_credit_card(
    request: CreateCreditCardRequest,
    handler: Annotated[CreateCreditCardHandlerContract, Depends(get_create_credit_card_handler)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    """Create a new credit card"""
    command = CreateCreditCardCommand(
        user_id=user_id,
        account_id=request.account_id,
        name=request.name,
        currency=request.currency,
        limit=request.limit,
    )

    result = await handler.handle(command)

    # Check for errors and map error codes to HTTP status codes
    if result.error_code:
        status_code_map = {
            CreateCreditCardErrorCode.NAME_ALREADY_EXISTS: 409,  # Conflict
            CreateCreditCardErrorCode.MAPPER_ERROR: 500,  # Internal Server Error
            CreateCreditCardErrorCode.UNEXPECTED_ERROR: 500,  # Internal Server Error
        }
        status_code = status_code_map.get(result.error_code, 500)
        raise HTTPException(status_code=status_code, detail=result.error_message)

    if result.credit_card_id is None:
        raise HTTPException(
            status_code=500,
            detail="credit card id is not present",
        )

    return CreateCreditCardResponse(
        credit_card_id=result.credit_card_id,
        name=request.name,
        limit=CardLimit.from_float(request.limit).value,
    )
