from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from app.context.user.domain.value_objects.user_id import UserID
from app.context.credit_card.application.commands.update_credit_card_command import (
    UpdateCreditCardCommand,
)
from app.context.credit_card.application.contracts.update_credit_card_handler_contract import (
    UpdateCreditCardHandlerContract,
)
from app.context.credit_card.domain.value_objects.card_limit import CardLimit
from app.context.credit_card.domain.value_objects.card_used import CardUsed
from app.context.credit_card.domain.value_objects.credit_card_id import CreditCardID
from app.context.credit_card.domain.value_objects.credit_card_name import (
    CreditCardName,
)
from app.context.credit_card.infrastructure.dependencies import (
    get_update_credit_card_handler,
)
from app.context.credit_card.interface.schemas.update_credit_card_response import (
    UpdateCreditCardResponse,
)
from app.context.credit_card.interface.schemas.update_credit_card_schema import (
    UpdateCreditCardRequest,
)

router = APIRouter(prefix="/cards", tags=["credit-cards"])


@router.put("/{credit_card_id}", response_model=UpdateCreditCardResponse)
async def update_credit_card(
    credit_card_id: int,
    request: UpdateCreditCardRequest,
    handler: UpdateCreditCardHandlerContract = Depends(get_update_credit_card_handler),
):
    """Update an existing credit card"""

    try:
        # Build optional value objects
        name: Optional[CreditCardName] = (
            CreditCardName(request.name) if request.name else None
        )
        limit: Optional[CardLimit] = (
            CardLimit.from_float(request.limit) if request.limit is not None else None
        )
        used: Optional[CardUsed] = (
            CardUsed.from_float(request.used) if request.used is not None else None
        )

        # Convert request to command
        # TODO: user_id from cookie header
        command = UpdateCreditCardCommand(
            credit_card_id=CreditCardID(credit_card_id),
            user_id=UserID(1),
            name=name,
            limit=limit,
            used=used,
        )

        # Handle the command
        result = await handler.handle(command)

        if not result.success:
            raise HTTPException(status_code=400, detail=result.error)

        return UpdateCreditCardResponse(
            success=True, message="Credit card updated successfully"
        )

    except ValueError as e:
        # Business logic errors (validation errors, etc.)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Unexpected errors
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )
