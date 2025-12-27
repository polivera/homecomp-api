from fastapi import APIRouter, Depends, HTTPException

from app.context.user.domain.value_objects.user_id import UserID
from app.context.credit_card.application.contracts.find_credit_card_by_id_handler_contract import (
    FindCreditCardByIdHandlerContract,
)
from app.context.credit_card.application.contracts.find_credit_cards_by_user_handler_contract import (
    FindCreditCardsByUserHandlerContract,
)
from app.context.credit_card.application.queries.find_credit_card_by_id_query import (
    FindCreditCardByIdQuery,
)
from app.context.credit_card.application.queries.find_credit_cards_by_user_query import (
    FindCreditCardsByUserQuery,
)
from app.context.credit_card.domain.value_objects.credit_card_id import CreditCardID
from app.context.credit_card.infrastructure.dependencies import (
    get_find_credit_card_by_id_handler,
    get_find_credit_cards_by_user_handler,
)
from app.context.credit_card.interface.schemas.credit_card_response import (
    CreditCardResponse,
)

router = APIRouter(prefix="/cards", tags=["credit-cards"])


@router.get("/{credit_card_id}", response_model=CreditCardResponse)
async def get_credit_card(
    credit_card_id: int,
    handler: FindCreditCardByIdHandlerContract = Depends(
        get_find_credit_card_by_id_handler
    ),
):
    """Get a credit card by ID"""

    try:
        # TODO: user_id from cookie header
        query = FindCreditCardByIdQuery(
            credit_card_id=CreditCardID(credit_card_id),
            user_id=UserID(1),
        )

        # Handle the query
        result = await handler.handle(query)

        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"Credit card with ID {credit_card_id} not found",
            )

        return CreditCardResponse(
            credit_card_id=result.credit_card_id,
            user_id=result.user_id,
            account_id=result.account_id,
            name=result.name,
            currency=result.currency,
            limit=result.limit,
            used=result.used,
        )

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


@router.get("", response_model=list[CreditCardResponse])
async def get_credit_cards(
    handler: FindCreditCardsByUserHandlerContract = Depends(
        get_find_credit_cards_by_user_handler
    ),
):
    """Get all credit cards for the current user"""

    try:
        # TODO: user_id from cookie header
        query = FindCreditCardsByUserQuery(user_id=UserID(1))

        # Handle the query
        results = await handler.handle(query)

        return [
            CreditCardResponse(
                credit_card_id=result.credit_card_id,
                user_id=result.user_id,
                account_id=result.account_id,
                name=result.name,
                currency=result.currency,
                limit=result.limit,
                used=result.used,
            )
            for result in results
        ]

    except ValueError as e:
        # Validation errors
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Unexpected errors
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )
