from fastapi import APIRouter, Depends, HTTPException

from app.context.credit_card.application.commands.create_credit_card_command import (
    CreateCreditCardCommand,
)
from app.context.credit_card.application.contracts.create_credit_card_handler_contract import (
    CreateCreditCardHandlerContract,
)
from app.context.credit_card.domain.value_objects.card_limit import CardLimit
from app.context.credit_card.infrastructure.dependencies import (
    get_create_credit_card_handler,
)
from app.context.credit_card.interface.schemas.create_credit_card_response import (
    CreateCreditCardResponse,
)
from app.context.credit_card.interface.schemas.create_credit_card_schema import (
    CreateCreditCardRequest,
)

router = APIRouter(prefix="/cards", tags=["credit-cards"])


@router.post("", response_model=CreateCreditCardResponse, status_code=201)
async def create_credit_card(
    request: CreateCreditCardRequest,
    handler: CreateCreditCardHandlerContract = Depends(get_create_credit_card_handler),
):
    """Create a new credit card"""

    try:
        # Convert request to command with value objects
        # TODO: user_id from cookie header
        command = CreateCreditCardCommand(
            user_id=1,
            account_id=request.account_id,
            name=request.name,
            currency=request.currency,
            limit=request.limit,
        )

        # Handle the command
        result = await handler.handle(command)
        if result.error is not None:
            raise HTTPException(status_code=400, detail=result.error)

        # Fetch the created card details to return complete response
        return CreateCreditCardResponse(
            credit_card_id=result.credit_card_id.value,
            name=request.name,
            limit=CardLimit.from_float(request.limit).value,
        )

    except ValueError as e:
        # Business logic errors (duplicate card, validation errors, etc.)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Unexpected errors
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )
