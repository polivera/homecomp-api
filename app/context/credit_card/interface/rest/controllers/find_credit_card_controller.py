from fastapi import APIRouter, Depends, HTTPException

from app.context.credit_card.application.contracts import (
    FindCreditCardByIdHandlerContract,
    FindCreditCardsByUserHandlerContract,
)
from app.context.credit_card.application.queries import (
    FindCreditCardByIdQuery,
    FindCreditCardsByUserQuery,
)
from app.context.credit_card.infrastructure.dependencies import (
    get_find_credit_card_by_id_handler,
    get_find_credit_cards_by_user_handler,
)
from app.context.credit_card.interface.schemas.credit_card_response import (
    CreditCardResponse,
)
from app.shared.infrastructure.middleware import get_current_user_id

router = APIRouter(prefix="/cards", tags=["credit-cards"])


@router.get("/{credit_card_id}", response_model=CreditCardResponse)
async def get_credit_card(
    credit_card_id: int,
    handler: FindCreditCardByIdHandlerContract = Depends(
        get_find_credit_card_by_id_handler
    ),
    user_id: int = Depends(get_current_user_id),
):
    """Get a credit card by ID"""
    query = FindCreditCardByIdQuery(
        credit_card_id=credit_card_id,
        user_id=user_id,
    )

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


@router.get("", response_model=list[CreditCardResponse])
async def get_credit_cards(
    handler: FindCreditCardsByUserHandlerContract = Depends(
        get_find_credit_cards_by_user_handler
    ),
    user_id: int = Depends(get_current_user_id),
):
    """Get all credit cards for the current user"""
    query = FindCreditCardsByUserQuery(user_id=user_id)

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
